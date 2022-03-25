from TestsRunner.modules.Selenium.Selenium import StepResultClass
from TestsRunner.modules.Selenium.Selenium import SeleniumClass
from TestsParser.modules.StepParser import *



class StepRunnerClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass):
        self.Config = Config
        self.Logger = Logger
        self.Selenium = SeleniumClass(Config, Logger)

    def RunStep(self, Step: StepClass, TestName: str, SegmentNumber: int, StepNumber: int) -> StepResultClass:
        try: HandymanExecution = Step.Action.split(".")[0]
        except Exception: 
            self.Logger.Log(f"В тесте {TestName} сегмент {SegmentNumber} шаге {StepNumber} возникла ошибка - некоректный параметр Action", "Error")
            return StepResultClass(False, "Некорректный блок Action")

        if(HandymanExecution == "Selenium"):
            return self.Selenium.RunStep(Step, TestName, SegmentNumber, StepNumber)
        else:
            self.Logger.Log(f"В тесте {TestName} сегмент {SegmentNumber} шаге {StepNumber} параметр Action возникла ошибка - неизвестный исполнитель", "Error")
            return StepResultClass(False, "Неизвестный исполнитель")
