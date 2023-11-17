class AppConfig:
    def __init__(self):
        self.file = open("app_config.conf", "w")
        self.keys = []
        self.username = ""
