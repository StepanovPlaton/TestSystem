import yaml
import codecs
from pathlib import Path

class YAMLReader:
    def ReadYamlFile(PathToFile: int):
        with codecs.open(Path(__file__).parents[0] / PathToFile, encoding='utf-8') as YAMLFile:
            return yaml.safe_load(YAMLFile)
            