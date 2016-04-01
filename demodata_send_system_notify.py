#!/usr/bin/env python

import os,sys,time,json,urllib2
from random import randint
from json import JSONEncoder

class Update:
  def __init__(self, name, version, arch, repository, baseversion):
    self.name = name
    self.version = version
    self.architecture = arch
    self.repository = repository
    self.baseversion = baseversion

class System:
  def __init__(self, name, urn, os, address, reboot_required):
    self.name = name
    self.urn = urn
    self.os = os
    self.address = address
    self.reboot_required = reboot_required
    self.packageupdates = list()

  def addUpdate(self, update):
    self.packageupdates.append(update)

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# Demodata
urn = 'vm1'
sys = System(urn, urn, "Ubuntu 15.10", "127.0.0.1", True)
sys.addUpdate(Update(name="vim", version="demoupdate", arch="amd64", repository="demorepo", baseversion="2:7.4.712-2ubuntu4"))
sys.addUpdate(Update(name="dnsutils", version="demoupdate", arch="amd64", repository="demorepo", baseversion="1:9.9.5.dfsg-11ubuntu1"))

#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/system/' + urn + '/notify'

print("Sending to server (notify system " + urn + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

