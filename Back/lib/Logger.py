from typing import Any
from lib.ConfigReader import ConfigClass


class LoggerError(Exception): pass

class UnknownLogLevel(LoggerError): pass
class NotSetLogLevel(LoggerError): pass

class LoggerClass():
    def __init__(self, Config: ConfigClass):
        self.Config = Config.Config
        self.Levels = ["All", "Debug", "Info", "Warning", "Error", "Broken"]

        self.NeedIndent = False

        try: self.CurrentLevel = self.Config['Logger']['LogLevel']
        except Exception: 
            self.Log("Ошибка загрузки системы логирования! Не установлен уровень логирования в config.yaml", "Broken")
            raise NotSetLogLevel()

        if(self.CurrentLevel not in self.Levels):
            self.Log("Ошибка загрузки системы логирования! Установлен неизвестный уровень логирования", "Broken")
            raise UnknownLogLevel()

    def Log(self, Message: str, Level: str ="Info") -> None:
        if(Level not in self.Levels): Level = "Info"
        if(self.Levels.index(Level) < self.Levels.index(self.CurrentLevel)): return

        if(Level == "All"):   print(f"{LogColors.OkCyan}", end="")
        if(Level == "Debug"):   print(f"{LogColors.OkBlue}", end="")
        if(Level == "Info"):    print(f"{LogColors.Bold}", end="")
        if(Level == "Warning"): print(f"{LogColors.Warning}", end="")
        if(Level == "Error"):   print(f"{LogColors.Error}", end="")
        if(Level == "Broken"):  print(f"{LogColors.Broke}", end="")
        print(f"{Message}{LogColors.End}")

        if(Level != "Debug"): self.NeedIndent = True

    def DebugPrint(self, *Messages: Any):
        print(f"{LogColors.OkBlue}{' '.join([str(i) for i in Messages])}{LogColors.End}")

    def Indent(self): 
        if(self.NeedIndent): 
            print() 
            self.NeedIndent = False
    def Detach(self): 
        if(self.NeedIndent): 
            print(f"\n{LogColors.OkCyan}--- --- --- --- ---{LogColors.End}\n")
            self.NeedIndent = False

class LogColors:
    Header = '\033[95m'
    
    OkBlue = '\033[94m'
    OkCyan = '\033[96m'
    OkGreen = '\033[92m'
    
    Warning = '\033[93m'
    Error = '\033[91m'
    Broke = '\033[91m\033[1m\033[4m'
    
    End = '\033[0m'

    Bold = '\033[1m'
    Underline = '\033[4m'