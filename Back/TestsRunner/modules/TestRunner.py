# --- --- ---
from Back.TestsRunner.modules.StepRunner import StepResult
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from TestsParser.modules.TestParser import TestClass
# --- --- ---

class TestResult:
    StepsResult = list[StepResult | None]

class TestRunnerClass:
    def RunTest(self, Test: TestClass):
        Test.