
from webbrowser import Chrome

from .SeleniumActionRunner import SeleniumActionRunnerClass, StepResultClass
from TestsParser.modules.StepParser import *

from selenium import webdriver #type:ignore

class SeleniumClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass) -> None:
        self.Config = Config.Config
        self.Logger = Logger
        self.SeleniumActionRunner = SeleniumActionRunnerClass()

        try: self.PathToChromeDriver: str = self.Config["Selenium"]["PathToChromeDriver"]
        except Exception: 
            self.Logger.Log("Ошибка загрузки Selenium агента! Не установлен путь до chromedriver.exe в config.yaml", "Broken")
            raise ValueError()

        self.WebDriver = Chrome(self.PathToChromeDriver)

    def RunStep(self, Step: StepClass, TestName: str, SegmentNumber: int, StepNumber: int) -> StepResultClass:
        Action = Step.Action.split(".")[1]
        if(Action == "Click"): return self.SeleniumActionRunner.Click(Step, self.WebDriver)

        else: return StepResultClass(False, f"Неизвестное действие {Step.Action} в тесте {TestName}, сегменте {SegmentNumber}, шаг #{StepNumber}")