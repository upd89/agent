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


sys = lib.sysinfo.get_notify_system()
sys = lib.pkg.addUpdates(sys)
jsondata = json.dumps(sys, cls=MyEncoder)

print(jsondata)
