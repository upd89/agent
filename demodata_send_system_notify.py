#!/usr/bin/env python

import os,sys,time,json,urllib2
from random import randint
from json import JSONEncoder

urn = 'vm1'
#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/system/' + urn + '/notify'

class System:
  def __init__(self, name, urn, os, address, reboot_required):
    self.name = name
    self.urn = urn
    self.os = os
    self.address = address
    self.reboot_required = reboot_required

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

sys = System(urn, urn, "Ubuntu 15.10", "127.0.0.1", True)

print("Sending to server (notify system " + urn + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

