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
    return __getBaseURL(_config) + "/system/" + urn + "/refresh-installed"


def getTaskNotifyURL(_config, taskid):
    return __getBaseURL(_config) + "/task/" + taskid + "/notify"


def push(url, data):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    answer = ''

    try:
        response = urllib2.urlopen(req, json.dumps(data, cls=MyEncoder))
        print(json.dumps(data, cls=MyEncoder))
        answer = response.read()
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))
    except Exception:
        print('generic exception')

    return answer


def pushRegister(_config, sys):
    url = getRegisterURL(_config)
    return push(url, sys)


def pushSystemNotify(_config, urn, sys):
    url = getSystemNotifyURL(_config, urn)
    return push(url, sys)


def pushSystemUpdateInstalled(_config, urn, packages):
    url = getSystemUpdateInstalledURL(_config, urn)
    return push(url, packages)

def pushTaskNotify(_config, taskid, tasknotify):
    url = getTaskNotifyURL(_config, taskid)
    return push(url, tasknotify)

