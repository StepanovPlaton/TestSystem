# --- --- ---
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from TestsParser.TestsParser import *
from TestsRunner.modules.TestRunner import *
# --- --- ---

class TestsRunnerClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass, TestsParser: TestsParserClass):
        self.Config = Config.Config
        self.Logger = Logger
        self.TestsParser = TestsParser
        self.TestRunner = TestRunnerClass()

    def RunTest(self, FullTestName: str) -> None:
        try: Test = self.TestsParser.GetTestByFullName(FullTestName)
        except TestsParserClass.TestNofFound: 
            self.Logger.Log(f"Тест {FullTestName} не найден в системе", "Error")
        else: return self.TestRunner.RunTest(Test)