class LoggerClass():
    def __init__(self, Config):
        self.Config = Config.Config
        self.Levels = ["Debug", "Info", "Warning", "Error", "Broken"]

        try: self.CurrentLevel = self.Config['Logger']['LogLevel']
        except Exception: 
            self.Log("Ошибка загрузки системы логирования! Не установлен уровень логирования в config.yaml", "Broken")
            raise NameError()

        if(self.CurrentLevel not in self.Levels):
            self.Log("Ошибка загрузки системы логирования! Установлен неизвестный уровень логирования", "Broken")
            raise ValueError()


    def Log(self, Message, Level ="Info"):
        if(Level not in self.Levels): Level = "Info"

        if(Level == "Debug"):   print(f"{LogColors.OkCyan}", end="")
        if(Level == "Info"):    print(f"{LogColors.Bold}", end="")
        if(Level == "Warning"): print(f"{LogColors.Warning}", end="")
        if(Level == "Error"):   print(f"{LogColors.Error}", end="")
        if(Level == "Broken"):  print(f"{LogColors.Error}{LogColors.Bold}{LogColors.Underline}", end="")
        print(f"{Message}{LogColors.End}")

    def Indent(self): print() 
    def Detach(self): print("----------")


class LogColors:
    Header = '\033[95m'
    
    OkBlue = '\033[94m'
    OkCyan = '\033[96m'
    OkGreen = '\033[92m'
    
    Warning = '\033[93m'
    Error = '\033[91m'
    
    End = '\033[0m'

    Bold = '\033[1m'
    Underline = '\033[4m'