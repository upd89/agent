#!/usr/bin/env python

import syspath
from upd89.classes.encoder import MyEncoder
from upd89.lib.configloader import ConfigLoader
import upd89.lib.sysinfo
import upd89.lib.pkg
import upd89.lib.log
import json


_config = ConfigLoader("config")
_logger = upd89.lib.log.screenLog()


sys = upd89.lib.sysinfo.get_notify_system()
sys = upd89.lib.pkg.addUpdates(sys)
jsondata = json.dumps(sys, cls=MyEncoder)

print(jsondata)
