from flask import Flask

from TestsParser.TestsParser import TestsParserClass

from lib.ConfigReader import *
from lib.Logger import *
from TestsParser import *

Config = ConfigClass()
Logger = LoggerClass(Config)

TestsParser = TestsParserClass(Config, Logger, YAMLReader)

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'
#app.run()
