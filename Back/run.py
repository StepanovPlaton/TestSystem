import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0]))
sys.path.append(str(Path(__file__).parents[0] / Path("./TestsRunner/.")))
sys.path.append(str(Path(__file__).parents[0] / Path("./TestsParser/.")))
# --- --- ---
from flask import Flask
# --- --- ---
from lib.ConfigReader import *
from lib.Logger import *
from lib.YAMLReader import *
from TestsParser.TestsParser import *
from TestsRunner.TestsRunner import *
# --- --- ---

YAMLReader = YAMLReaderClass()
Config = ConfigClass(YAMLReader)
Logger = LoggerClass(Config)

TestsParser = TestsParserClass(Config, Logger, YAMLReader)
TestsRunner = TestsRunnerClass(Config, Logger, TestsParser)
print(TestsRunner.RunTest("test")[0][0].ErrorDescription)

app = Flask(__name__)
@app.route('/') #type: ignore
def hello_world():
    return 'Hello World!'
#app.run()