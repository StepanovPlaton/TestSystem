import os
from pathlib import Path as Path_

# --- --- ---
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from modules.DataParser import *
from modules.StepParser import *
# --- --- ---

class MacroClass:
    def __init__(self):
        self.Name: str
        self.Description: str
        self.Steps: list[StepClass | MacroClass]

    def __str__(self) -> str:
        return f"Макрос \"{self.Name}\" - {len(self.Steps)} действий(я)"

    def __repr__(self) -> str:
        return f"<{self.__str__()}>"

    class ActionsBlockNotFound(Exception): pass


class MacrosParserClass:
    class MacroFolderNotFound(Exception): pass
    class NestedMacrosCycle(Exception): pass
    class MacroNotFound(Exception): pass

    def __init__(self, Config: dict[str, Any], Logger: LoggerClass, YAMLReader: YAMLReaderClass):
        self.Config = Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader
        self.StepParser = StepParserClass(Logger, YAMLReader)

        try: self.RelativePathToMacrosFolder = self.Config["Paths"]["MacroFolder"]
        except Exception: 
            self.Logger.Log("Ошибка загрузки системы парсинга макросов тестирования! Не установлен путь до папки с макросами в config.yaml", "Broken")
            raise MacrosParserClass.MacroFolderNotFound()

        self.PathToMacrosFolder = self.Config["ParserRootPath"] / self.RelativePathToMacrosFolder
        self.Macros = self.ParsMacros(self.PathToMacrosFolder, self.PathToMacrosFolder)

        self.Logger.Indent()
        self.Logger.Log(f"Полученное древо макросов:{DictToTree(self.Macros)}", "Info")
        self.Logger.Detach()

    def ParsMacros(self, Path: str, RootPath: str, FullAccumulatedName: str ="") -> dict[str, Any]:
        Macros: dict[str, Any] = {}
        Elements = os.listdir(Path)
        for Element in Elements:
            ElementPath = os.path.join(Path, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                try: ParsedMacro = self.ParsMacro(Element, ElementPath, RootPath, 
                                                    FullAccumulatedName+f"{Element.replace('.yaml', '')}", [])
                except Exception: pass
                else: Macros[Element] = ParsedMacro
            elif(os.path.isdir(ElementPath)):
                # is Folder
                Macros[Element] = self.ParsMacros(ElementPath, RootPath, FullAccumulatedName+f"{Element}.")
                self.Logger.Indent()
        return Macros

    def ParsMacro(self, Element: str, Path: str, RootPath: str, FullAccumulatedName: str, NestedMacros: list[str] =[]) -> MacroClass:
        Macro: MacroClass = MacroClass()
        try:
            YamlMacro = self.YAMLReader.ReadYamlFile(Path)
        except Exception:
            self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как повреждён или содержит неправильный синтаксис", "Error")
            raise YAMLReaderClass.YamlIncorrectSyntax()
        else:
            try: Macro.Name = YamlMacro["MacroName"]
            except Exception: pass

            try: Macro.Description = YamlMacro["Description"]
            except Exception: pass

            try: Actions = YamlMacro["Actions"]
            except Exception: 
                self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как не содержит блок Actions", "Error")
                raise MacroClass.ActionsBlockNotFound()
            else: 
                Macro.Steps = []
                for i, Step in enumerate(Actions):
                    try: ParsedStep = self.StepParser.ParseStep((Step), f"{Element} шаг #{i+1}")
                    except Exception: 
                        self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как в одном из шагов обнаружена ошибка", "Error")
                        raise StepParserClass.StepParsingError()
                    else:
                        if(ParsedStep.StepType == "Action"): Macro.Steps.append(ParsedStep)
                        else:
                            # Вложенный макрос
                            NestedMacros.append(FullAccumulatedName)
                            if(ParsedStep.Macro in NestedMacros):
                                if(FullAccumulatedName == ParsedStep.Macro):
                                    self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как содержит цикличный вызов {ParsedStep.Macro} на шаге #{i+1}", "Error")
                                raise MacrosParserClass.NestedMacrosCycle()

                            try:
                                PathToNestedMacro: str = \
                                    str(Path_(RootPath).joinpath(self.GetPathtoMacroFromName(ParsedStep.Macro, RootPath)[1:]))
                            except MacrosParserClass.MacroNotFound: 
                                self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как содержит вызов макроса, который не удалось найти в системе - {ParsedStep.Macro} ", "Error")
                                raise MacrosParserClass.MacroNotFound()

                            try: NestedMacro = self.ParsMacro(
                                    f"{Element}/Шаг #{i+1}/{ParsedStep.Macro}", 
                                    PathToNestedMacro, 
                                    RootPath,
                                    ParsedStep.Macro,
                                    NestedMacros)
                            except MacrosParserClass.NestedMacrosCycle:
                                if(Element.find("Шаг") == -1):
                                    self.Logger.Log(f"Макрос {FullAccumulatedName+'.yaml'} был пропущен, так как содержит цикличный вызов {ParsedStep.Macro} на шаге #{i+1}", "Error")
                                raise
                            else:
                                Macro.Steps.append(NestedMacro)
                return Macro

    def GetPathtoMacroFromName(self, MacroName: str, RootPath: str, Path: str="") -> str:
        SearchedElement = MacroName.split(".")[0]
        Elements = os.listdir(RootPath)
        for Element in Elements:
            ElementPath = os.path.join(RootPath, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                if(Element.replace(".yaml", "") == SearchedElement):
                    return f"{Path}/{Element}"
            elif(os.path.isdir(ElementPath)):
                # is Folder
                try:
                    return self.GetPathtoMacroFromName(".".join(MacroName.split(".")[1:]), ElementPath, f"{Path}/{Element}")
                except MacrosParserClass.MacroNotFound: pass
        raise MacrosParserClass.MacroNotFound()

    def GetMacroByFullName(self, FullName: str, Macros: dict[str, Any] | None =None) -> MacroClass:
        if(Macros is None): return self.GetMacroByFullName(FullName, self.Macros)

        if(FullName.find(".") != -1):
            BranchName = FullName.split(".")[0]
            try: Branch = Macros[BranchName]
            except Exception: raise MacrosParserClass.MacroNotFound()
            return self.GetMacroByFullName(".".join(FullName.split(".")[1:]), Branch)
        else: 
            try: Macro = Macros[FullName]
            except Exception: raise MacrosParserClass.MacroNotFound()
            return Macro

