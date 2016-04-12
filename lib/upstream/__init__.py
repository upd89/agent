import json,urllib2

from classes.encoder import MyEncoder

def getRegisterURL(_config):
  return _config.getServerURL() + _config.getApiVersion() + "/register"

def getSystemNotifyURL(_config, urn):
  return _config.getServerURL() + _config.getApiVersion() + "/system/" + urn + "/notify"

def getSystemUpdateInstalledURL(_config, urn):
  return _config.getServerURL() + _config.getApiVersion() + "/system/" + urn + "/updateInstalled"

def getTaskNotifyURL(_config, taskid):
  return _config.getServerURL() + _config.getApiVersion() + "/task/" + taskid + "/notify"

def push(url, data):
  req = urllib2.Request(url)
  req.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(req, json.dumps(data, cls=MyEncoder))
  return response.read()

