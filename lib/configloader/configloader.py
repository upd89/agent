import configparser
import os.path

class ConfigLoader:

    def __init__(self, configname):
        self.config = configparser.ConfigParser()
        self.configname = configname
        self.config.read(self.configname)

    def __str__(self):
        return repr(self)

    def getServerURL(self):
        return(self.config['server']['url'])

    def getApiVersion(self):
        return(self.config['api']['version'])

    def getLogFile(self):
        return(self.config['log']['file'])

    def getPidFile(self):
        return(self.config['daemon']['pidfile'])

    def getUUID(self):
        return self.__ret_if_exists('general', 'my_uuid')

    def setUUID(self, uuid):
        self.__set_config('general', 'my_uuid', uuid)

    def reloadConfig(self):
        self.config.read(self.configname)

    def __set_config(self, group, tag, value):
        self.config[group][tag] = value
        with open(self.configname, 'w') as configfile:
            self.config.write(configfile)

    def __ret_if_exists(self, group, tag):
        if self.config.has_option(group, tag):
            return(self.config[group][tag])
        else:
            return None
