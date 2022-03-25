from webbrowser import Chrome
from TestsParser.modules.StepParser import StepClass

class StepResultClass:
    Status: bool
    PathToScreenshot: str
    ErrorDescription: str
    def __init__(self, Status: bool =False, ErrorDescription: str = "") -> None:
        self.Status = Status
        self.ErrorDescription = ErrorDescription

class SeleniumActionRunnerClass:
    def Click(self, Step: StepClass, Driver: Chrome) -> StepResultClass:
        return StepResultClass(True, "Complete")
