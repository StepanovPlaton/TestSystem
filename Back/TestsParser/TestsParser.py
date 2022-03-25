import os

# --- --- ---
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from modules.DataParser import DataParserClass
from modules.MacrosParser import MacrosParserClass
from modules.TestParser import MacrosParserClass
from modules.TestParser import TestParserClass
from lib.DictionaryFormater import *
from TestsParser.modules.TestParser import *
# --- --- ---

class TestsParserClass():
    class TestsFolderNotFound(Exception): pass
    class TestNofFound(Exception): pass

    def __init__(self, Config: ConfigClass, Logger: LoggerClass, YAMLReader: YAMLReaderClass):
        self.Config = Config.Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader


        self.DataParser = DataParserClass(self.Config, Logger, YAMLReader)
        self.MacrosParser = MacrosParserClass(self.Config, Logger, YAMLReader)
        self.TestParser = TestParserClass(self.Config, Logger, YAMLReader, self.MacrosParser)

        try: self.RelativePathToTestsFolder: str = self.Config["Paths"]["TestsFolder"]
        except Exception: 
            self.Logger.Log("Ошибка загрузки системы парсинга тестов! Не установлен путь до папки с тестами в config.yaml", "Broken")
            raise TestsParserClass.TestsFolderNotFound()
        self.PathToTestsFolder = self.Config["ParserRootPath"] / self.RelativePathToTestsFolder
        
        self.Tests = self.ParsTests(self.PathToTestsFolder)
        print(DictToTree(self.Tests))

    def ParsTests(self, Path: str) -> dict[str, Any]:
        Tests: dict[str, Any] = {}
        Elements = os.listdir(Path)
        for Element in Elements:
            ElementPath = os.path.join(Path, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                try:
                    Tests[Element.replace(".yaml", "")] = self.TestParser.ParsTest(Element, ElementPath)
                except YAMLReaderClass.YamlIncorrectSyntax:
                    self.Logger.Log(f"Файл теста {Element} пропущен, так как повреждён или содержит неправильный синтаксис", "Error")
            elif(os.path.isdir(ElementPath)):
                # is Folder
                Tests[Element] = self.ParsTests(ElementPath)
        return Tests

    def GetTestByFullName(self, FullName: str, Tests: dict[str, Any] | None = None) -> TestClass:
        if(Tests is None): return self.GetTestByFullName(FullName, self.Tests)

        if(FullName.find(".") != -1):
            BranchName = FullName.split(".")[0]
            try: Branch = Tests[BranchName]
            except Exception: raise TestsParserClass.TestNofFound()
            else: return self.GetTestByFullName(".".join(FullName.split(".")[1:]), Branch)
        else: 
            try: Test = Tests[FullName]
            except Exception: raise TestsParserClass.TestNofFound()
            else: return Test
