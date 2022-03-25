# --- --- ---
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from modules.DataParser import *
from modules.StepParser import *
from modules.MacrosParser import *
# --- --- ---

class TestClass:
    class Segment:
        Name: str
        Description: str
        Actions: list[StepClass]

        #def __init__(self, Actions: list[StepClass | MacroClass]):
        #    self.Actions = Actions
        
    Name: str
    Number: str
    Description: str
    Tags: list[str]
    Segments: list[Segment]

class TestParserClass:
    class SegmentsAndActionsBlockAtTheSameTime(Exception): pass
    class MissingBothSegmentsAndActions(Exception): pass
    class SegmentNotContainsActionsBlock(Exception): pass
    class SegmentActionsParsingError(Exception): pass

    def __init__(self, Config: dict[str, Any], Logger: LoggerClass, YAMLReader: YAMLReaderClass, MacrosParser: MacrosParserClass) -> None:
        self.Config = Config
        self.Logger = Logger
        self.YamlReader = YAMLReader
        self.MacrosParser = MacrosParser
        self.StepParser = StepParserClass(self.Logger, self.YamlReader)


    def ParsTest(self, Element: str, Path: str) -> TestClass:
        Test: TestClass = TestClass()
        try: File = self.YamlReader.ReadYamlFile(Path)
        except YAMLReaderClass.YamlIncorrectSyntax:
            self.Logger.Log(f"Файл теста {Element} был пропущен, так как повреждён или содержит некоректный синтаксис", "Error")
            raise
        
        Test.Name = str(self.YamlReader.TryGetNesting(File, "Name"))
        Test.Number = str(self.YamlReader.TryGetNesting(File, "Number"))
        Test.Description = str(self.YamlReader.TryGetNesting(File, "Description"))

        try: _ = File["Tags"]
        except Exception: pass
        else:
            if(File["Tags"] is list):
                Test.Tags = [str(i) for i in File["Tags"]]

        ActionsFound: bool = True
        SegmentsFound: bool = True

        try: _ = File["Actions"]
        except Exception: ActionsFound = False
        try: _ = File["Segments"]
        except Exception: SegmentsFound = False

        if(ActionsFound and SegmentsFound):
            self.Logger.Log(f"Файл теста {Element} был пропущен, так как содежит неправильный смысловой синтаксис - eсть и блок Acntions, и блок Segments", "Error")
            raise TestParserClass.SegmentsAndActionsBlockAtTheSameTime()
        elif(not ActionsFound and not SegmentsFound):
            self.Logger.Log(f"Файл теста {Element} был пропущен, так как не содежит ни блок Acntions, ни блок Segments", "Error")
            raise TestParserClass.MissingBothSegmentsAndActions()
        else:
            Test.Segments = []
            if(ActionsFound): 
                Segment: TestClass.Segment = TestClass.Segment()
                Segment.Actions = self.ParsSegmentActions(File["Actions"], Element)
                Test.Segments.append(Segment)
            if(SegmentsFound): 
                for SegmentYaml in File["Segments"]:
                    Segment: TestClass.Segment = TestClass.Segment()
                    Segment.Name = str(self.YamlReader.TryGetNesting(SegmentYaml, "Name"))
                    Segment.Description = str(self.YamlReader.TryGetNesting(SegmentYaml, "Description"))
                    try: SegmentActions = SegmentYaml["Actions"]
                    except Exception: 
                        self.Logger.Log(f"В одном из сегментов теста {Element} отсутствует блок Actions", "Error")
                        raise TestParserClass.SegmentNotContainsActionsBlock()
                    Segment.Actions = self.ParsSegmentActions(SegmentActions, Element)
                    Test.Segments.append(Segment)
        return Test


    def ParsSegmentActions(self, Actions: list[dict[str, Any]], Element: str) -> list[StepClass]:
        Segment: list[StepClass] = []
        for Action in Actions:
            Step = self.StepParser.ParseStep(Action)
            if(Step.isMacro()):
                try: self.MacrosParser.GetMacroByFullName(Step.Macro)
                except Exception: 
                    self.Logger.Log(f"Ошибка при разборе одного из действий теста {Element}, обнаружен неизвестный макрос {Step.Macro}", "Error")
                    raise TestParserClass.SegmentActionsParsingError()
            Segment.append(Step)

        return Segment