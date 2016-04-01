#!/usr/bin/env python

import os,sys,time,apt,json,urllib2
from random import randint

from classes.package import Package
from classes.packagelist import Packagelist
from classes.encoder import MyEncoder

urn = 'vm1'
#url = 'http://upd89.org/api.php'
url = 'http://cc.upd89.org/v1/system/' + urn + '/updateInstalled'

print("Reading local cache...")
cache = apt.Cache()

packages = Packagelist()
for pkg in cache:
   if (pkg.is_installed):
      pkg_base = pkg.versions[-1]
      pkg_origin = pkg_base.origins[0]
      repo_string = pkg_origin.origin + "_" + pkg_origin.archive + "_" + pkg_origin.component
      packages.add(Package(name=pkg.name, version=pkg.installed.version,
                       arch=pkg.architecture(), baseversion=pkg_base.version,
                       section=pkg.section, homepage=pkg.installed.homepage,
                       summary=pkg.installed.summary, repo=repo_string))

print("Sending to server...")
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(packages, cls=MyEncoder))
print("Response:")
print(response.read())

