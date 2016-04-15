import logging


class Log:

    def __init__(self, _config):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.fh = logging.FileHandler(_config.getLogFile(), "w")
        self.fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
        self.keep_fds = [self.fh.stream.fileno()]

    def getLogger(self):
        return self.logger

    def getKeepfds(self):
        return self.keep_fds
