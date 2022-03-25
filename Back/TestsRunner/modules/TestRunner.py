# --- --- ---
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from TestsParser.modules.TestParser import *
from TestsRunner.modules.StepRunner import *
from TestsRunner.modules.MacroRunner import *
# --- --- ---

SegmentResultClass = list[StepResultClass | MacroResultClass]
TestResultClass = list[SegmentResultClass]

class TestRunnerClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass):
        self.Logger = Logger
        self.StepRunner = StepRunnerClass(Config, Logger)

    def RunTest(self, Test: TestClass) -> TestResultClass:
        TestResult: TestResultClass = []
        for SegmentNumber, Segment in enumerate(Test.Segments):
            SegmentResult: SegmentResultClass = []
            for StepNumber, Step in enumerate(Segment.Actions):
                if(Step.isMacro()):
                    pass
                else:
                    SegmentResult.append(self.StepRunner.RunStep(Step, Test.Name, SegmentNumber, StepNumber))
            TestResult.append(SegmentResult)        
        return TestResult