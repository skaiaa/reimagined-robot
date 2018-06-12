class Logger:
    def __init__(self):
        self._appender = print

    def log(self, log):
        self._appender(log)

    def set_appender(self, appender):
        self._appender = appender


logger = Logger()
