
from pathlib import Path

class Settings:
    def __init__(self):
        self.basedir = Path.cwd()
        self.rawdir = self.basedir / "C:\\Users\\xande\\PycharmProjects\\DEDS\\DEDS Portfolio\\week1\\Data"
        self.processeddir = self.basedir / "C:\\Users\\xande\\PycharmProjects\\DEDS\\DEDS Portfolio\\week1\\Data\\Vragen"
        self.logdir = self.basedir / "log"

settings = Settings()