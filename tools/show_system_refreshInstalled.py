#!/usr/bin/env python

import syspath
from classes.encoder import MyEncoder
from lib.configloader import ConfigLoader
import lib.sysinfo
import lib.pkg
import lib.log
import json


_config = ConfigLoader("config")
_logger = lib.log.screenLog()

packages = lib.pkg.getPackageList()
jsondata = json.dumps(packages, cls=MyEncoder)

print(jsondata)
