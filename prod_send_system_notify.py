#!/usr/bin/env python

import os,sys,time,apt,json,socket,platform
import json,urllib2

import tools
from classes.update import Update
from classes.system_notify import System
from classes.encoder import MyEncoder

myHostname = socket.gethostname()
myURN = 'demo-' + myHostname + '-demo'
myDistro = ' '.join(platform.linux_distribution())
myIP = tools.get_ip()
needReboot = os.path.isfile("/var/run/reboot-required")

#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/system/' + myURN + '/notify'

sys = System(name=myHostname, urn=myURN, os=myDistro, address=myIP, reboot_required=needReboot)

#if os.geteuid() != 0:
#    exit("You need to have root privileges to run this script.")

print("Reading local cache...")
cache = apt.Cache()

#print("Updating cache...")
#try:
#   cache.update()
#except:
#   print("had some troubles, but anyway, let's go on...")

print("Reading Upgradable Packages...")
for pkg in cache:
   if (pkg.is_upgradable):
      #print(pkg.name)
      pkg_base = pkg.versions[-1]
      pkg_origin = pkg.versions[0].origins[0]
      repo_string = pkg_origin.origin + "_" + pkg_origin.archive + "_" + pkg_origin.component
      sys.addUpdate(Update(
           name        = pkg.name,
           version     = pkg.candidate.version,
           arch        = pkg.architecture(),
           repository  = repo_string,
           baseversion = pkg_base.version
      ))

print("Sending to server (notify system " + myURN + ")...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(sys, cls=MyEncoder))
print("Response:")
print(response.read())

