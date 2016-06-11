#!/usr/bin/env python

import syspath
from classes.encoder import MyEncoder
from upd89.lib.configloader import ConfigLoader
import upd89.lib.sysinfo
import upd89.lib.pkg
import upd89.lib.log
import json


_config = ConfigLoader("config")
_logger = upd89.lib.log.screenLog()

packages = upd89.lib.pkg.getPackageList()
jsondata = json.dumps(packages, cls=MyEncoder)

print(jsondata)
