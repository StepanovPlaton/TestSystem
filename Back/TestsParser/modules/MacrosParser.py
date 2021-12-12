from pathlib import Path as Path_
import os
from .StepParser import *
class MacrosParserClass:
    def __init__(self, Config, Logger, YAMLReader, DataParser):
        self.Config = Config.Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader
        self.DataParser = DataParser
        self.StepParser = StepParserClass(Logger)

        try: self.RelativePathToMacrosFolder = self.Config["Paths"]["MacroFolder"]
        except Exception: 
            self.Log("Ошибка загрузки системы парсинга макросов тестирования! Не установлен путь до папки с макросами в config.yaml", "Broken")
            raise

        self.PathToMacrosFolder = self.Config["ParserRootPath"] / self.RelativePathToMacrosFolder
        self.Macros = self.ParsMacros(self.PathToMacrosFolder)
        print(self.Macros)

    def ParsMacros(self, RootPath, FullAccumulatedName=""):
        Macros = {}
        Elements = os.listdir(RootPath)
        for Element in Elements:
            ElementPath = os.path.join(RootPath, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                ParsedMacro = self.ParsMacro(Element, ElementPath, RootPath, FullAccumulatedName+f"{Element}")
                if(not (ParsedMacro is None)): Macros[Element] = ParsedMacro
            elif(os.path.isdir(ElementPath)):
                # is Folder
                Macros[Element] = self.ParsMacros(ElementPath, FullAccumulatedName+f"{Element}.")
        return Macros

    def ParsMacro(self, Element, Path, RootPath, FullAccumulatedName, NestedMacros=[]):
        Macro = MacroClass()
        try:
            YamlMacro = self.YAMLReader.ReadYamlFile(Path)
        except Exception:
            self.Logger.Log(f"Макрос {Element} был пропущен, так как повреждён или содержит неправильный синтаксис", "Error")
        else:
            try: Macro.Name = YamlMacro["MacroName"]
            except Exception: pass

            try: Macro.Description = YamlMacro["Description"]
            except Exception: pass

            try: Actions = YamlMacro["Actions"]
            except Exception: self.Logger.Log(f"Макрос {Element} был пропущен, так как не содержит блок Actions", "Error")
            else: 
                FileCorrect = True
                for i, Step in enumerate(Actions):
                    try: ParsedStep = self.StepParser.ParseStep((Step), f"{Element} шаг {i+1}")
                    except Exception: 
                        self.Logger.Log(f"Макрос {Element} был пропущен, так как в одном из шагов обнаружена ошибка", "Error")
                        FileCorrect = False
                        break
                    else:
                        if(ParsedStep.StepType == "Action"): Macro.Steps.append(ParsedStep)
                        else:
                            # Вложенный макрос
                            PathToNestedMacro = RootPath.joinpath(self.GetPathtoMacroFromName(ParsedStep.Macro, RootPath)[1:])
                            NestedMacros.append(FullAccumulatedName)
                            NestedMacro = self.ParsMacro(
                                f"{Element}/Шаг #{i+1}/{ParsedStep.Macro}", 
                                PathToNestedMacro, 
                                RootPath,
                                NestedMacros)
                            print(NestedMacro)
                if(FileCorrect): return Macro
                else: return None

    def GetPathtoMacroFromName(self, MacroName, RootPath, Path=""):
        SearchedElement = MacroName.split(".")[0]
        #MacroName = ".".join(MacroName.split(".")[1:])
        Elements = os.listdir(RootPath)
        for Element in Elements:
            ElementPath = os.path.join(RootPath, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                if(Element.replace(".yaml", "") == SearchedElement):
                    return f"{Path}/{Element}"
            elif(os.path.isdir(ElementPath)):
                # is Folder
                return self.GetPathtoMacroFromName(".".join(MacroName.split(".")[1:]), ElementPath, f"{Path}/{Element}")
        return None

class MacroClass:
    def __init__(self):
        self.Name = ""
        self.Description = ""
        self.Steps = []

    def __str__(self):
        return f"Макрос \"{self.Name}\" - {len(self.Steps)} действий(я)"

    def __repr__(self):
        return f"<Макрос \"{self.Name}\" - {len(self.Steps)} действий(я)>"