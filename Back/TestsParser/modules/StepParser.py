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

class StepParserClass:
    def __init__(self, Logger):
        self.Logger = Logger

    def ParseStep(self, YamlStep, Location=""):
        Step = StepClass()
        
        ActionFound = True
        MacroFound = True

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



        try: Step.Descripton = YamlStep["Description"]
        except Exception: pass

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