from .YAMLReader import *
from pathlib import Path

class ConfigClass():
    def __init__(self, PathToConfig="..\config.yaml"): 
        try:
            self.Config = YAMLReader.ReadYamlFile(PathToConfig)
        except Exception:
            print('\033[91m\033[1m\033[4m'+"Ошибка чтения config.yaml"+'\033[0m')
            raise

        self.Config["ParserRootPath"] = Path(__file__).parents[1]