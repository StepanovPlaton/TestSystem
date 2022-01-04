from typing import Any

# --- --- ---
from lib.Logger import *
from lib.YAMLReader import *
# --- --- ---

class StepClass:
    def __init__(self):
        self.StepType = ""
        self.Action = ""
        self.Macro = ""

        self.Descripton = ""
        
        self.Locator = ""
        self.LocatorType = ""
        
        self.Optional = False
        self.Screenshot = False

    def __str__(self):
        return f"Действие {self.Action}"

    def __repr__(self):
        return f"(Действие {self.Action})"

    def isMacro(self): return not (self.Macro == "")

class StepParserClass:
    class StepParsingError(Exception): pass

    def __init__(self, Logger: LoggerClass, YamlReader: YAMLReaderClass):
        self.Logger = Logger
        self.YamlReader = YamlReader

    def ParseStep(self, YamlStep: dict[str, Any], Location: str=""):
        Step = StepClass()
        
        ActionFound: bool = True
        MacroFound: bool = True

        try: Step.Action = YamlStep["Action"]
        except Exception: ActionFound = False
        try: Step.Macro = YamlStep["Macro"]
        except Exception: MacroFound = False

        if(ActionFound and MacroFound):
            self.Logger.Log(f"В {Location} обнаружен и Action, и Macro", "Error")
            raise ValueError()
        elif(not ActionFound and not MacroFound):
            self.Logger.Log(f"В {Location} не обнаружен ни Action, ни Macro", "Error")
            raise ValueError()
        else:
            if(ActionFound): Step.StepType = "Action"
            if(MacroFound): Step.StepType = "Macro"


        Step.Descripton = self.YamlReader.TryGetNesting(YamlStep, "Description")

        try: _ = YamlStep["Locator"]
        except Exception: pass
        else:
            LocatorTypes = ["xpath", "id"]
            for LocatorType in LocatorTypes:
                if(LocatorType in YamlStep["Locator"].keys()):
                    Step.LocatorType = LocatorType
                    Step.Locator = YamlStep["Locator"][LocatorType]
                    break

        return Step