import json
import urllib2

from classes.encoder import MyEncoder


def __getBaseURL(_config):
    return _config.getServerURL() + _config.getApiVersion()


def getRegisterURL(_config):
    return __getBaseURL(_config) + "/register"


def getSystemNotifyURL(_config, urn):
    return __getBaseURL(_config) + "/system/" + urn + "/notify"


def getSystemUpdateInstalledURL(_config, urn):
    return __getBaseURL(_config) + "/system/" + urn + "/updateInstalled"


def getTaskNotifyURL(_config, taskid):
    return __getBaseURL(_config) + "/task/" + taskid + "/notify"


def push(url, data):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data, cls=MyEncoder))
    return response.read()


def pushRegister(_config, sys):
    url = getRegisterURL(_config)
    return push(url, sys)


def pushSystemNotify(_config, urn, sys):
    url = getSystemNotifyURL(_config, urn)
    return push(url, sys)


def pushSystemUpdateInstalled(_config, urn, packages):
    url = getSystemUpdateInstalledURL(_config, urn)
    return push(url, packages)
