# --- --- ---
from TestsRunner.modules.Selenium.Selenium import StepResultClass
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
from TestsParser.modules.TestParser import *
from TestsRunner.modules.StepRunner import *
# --- --- ---

class MacroResultClass:
    StepsResult = list[StepResultClass]