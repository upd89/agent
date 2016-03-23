#!/usr/bin/env python

import os,sys,time,apt,json
import json,urllib2
from json import JSONEncoder

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.")

class Package:
  def __init__(self, name, arch, installed, candidate, section):
    self.name = name
    self.arch = arch
    self.installed = installed
    self.candidate = candidate
    self.section = section

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__  

print("Reading local cache...")
cache = apt.Cache()
print("Updating cache...")
try:
   cache.update()
except:
   print("had some troubles, but anyway, let's go on...")

l = list()
print("Upgradable Packages:")
for pkg in cache:
   if (pkg.is_upgradable):
      print(pkg.name)
      l.append(Package(pkg.name, pkg.architecture(), pkg.installed.version, pkg.candidate.version, pkg.section))

print("Sending to server...")
req = urllib2.Request('http://upd89.org/api.php')
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(l, cls=MyEncoder))
print("Response:")
print(response.read())

