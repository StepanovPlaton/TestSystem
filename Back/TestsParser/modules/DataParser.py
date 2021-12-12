from pathlib import Path
import os

class DataParserClass:
    def __init__(self, Config, Logger, YAMLReader):
        self.Config = Config.Config
        self.Logger = Logger
        self.YAMLReader = YAMLReader

        try: self.RelativePathToDataFolder = self.Config["Paths"]["DataFolder"]
        except Exception: 
            self.Log("Ошибка загрузки системы парсинга данных тестирования! Не установлен путь до папки с данными в config.yaml", "Broken")
            raise
        
        self.PathToDataFolder = self.Config["ParserRootPath"] / self.RelativePathToDataFolder
        
        self.Data = self.ParsData(self.PathToDataFolder)
        self.Logger.Indent()

    def ParsData(self, Path):
        Data = {}
        Files = os.listdir(Path)
        for Element in Files:
            ElementPath = os.path.join(Path, Element)
            if(os.path.isfile(ElementPath)): 
                # is File
                try:
                    Data[Element.replace(".yaml", "")] = self.YAMLReader.ReadYamlFile(ElementPath)
                except Exception:
                    self.Logger.Log(f"Файл данных {Element} пропущен, так как повреждён или содержит неправильный синтаксис", "Error")
            elif(os.path.isdir(ElementPath)):
                # is Folder
                Data[Element] = self.ParsData(ElementPath)
        return Data