#!/usr/bin/env python

import os,sys,time,apt,socket

from lib.configloader.configloader import ConfigLoader
from classes.package import Package
from classes.packagelist import Packagelist
import lib.upstream

_config = ConfigLoader("config")

myHostname = socket.gethostname()
myURN = 'demo-' + myHostname + '-demo'
url = lib.upstream.getSystemUpdateInstalledURL(_config, myURN)

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

print("Sending to server (updateInstalled " + myHostname + ")...")
print(url)
response = lib.upstream.push(url, packages)
print("Response:\n" + response)

