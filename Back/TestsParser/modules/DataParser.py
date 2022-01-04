from pathlib import Path
import os

# --- --- ---
from lib.DictionaryFormater import *
from lib.YAMLReader import *
from lib.ConfigReader import *
from lib.Logger import *
# --- --- ---

class DataParserClass:
    def __init__(self, Config: dict[str, Any], Logger: LoggerClass, YAMLReader: YAMLReaderClass):
        self.Config = Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader

        try: self.RelativePathToDataFolder: str = self.Config["Paths"]["DataFolder"]
        except Exception: 
            self.Logger.Log("Ошибка загрузки системы парсинга данных тестирования! Не установлен путь до папки с данными в config.yaml", "Broken")
            raise
        
        self.PathToDataFolder: str = str(self.Config["ParserRootPath"] / Path(self.RelativePathToDataFolder))
        
        self.Data = self.ParsData(self.PathToDataFolder)
        
        self.Logger.Indent()
        self.Logger.Log(f"Полученное древо данных:{DictToTree(self.Data)}", "Info")
        self.Logger.Detach()

    def ParsData(self, Path: str) -> dict[str, Any]:
        Data: dict[str, Any] = {}
        Elements = os.listdir(Path)
        for Element in Elements:
            ElementPath = os.path.join(Path, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                try:
                    Data[Element.replace(".yaml", "")] = self.YAMLReader.ReadYamlFile(ElementPath)
                except YAMLReaderClass.YamlIncorrectSyntax:
                    self.Logger.Log(f"Файл данных {Element} пропущен, так как повреждён или содержит неправильный синтаксис", "Error")
            elif(os.path.isdir(ElementPath)):
                # is Folder
                Data[Element] = self.ParsData(ElementPath)
        return Data