from .modules.DataParser import DataParserClass
from .modules.MacrosParser import MacrosParserClass

class TestsParserClass():
    def __init__(self, Config, Logger, YAMLReader):
        self.Config = Config.Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader

        self.DataParser = DataParserClass(Config, Logger, YAMLReader)
        self.MacrosParser = MacrosParserClass(Config, Logger, YAMLReader, self.DataParser)