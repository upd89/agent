#!/usr/bin/env python

import syspath
from lib.configloader import ConfigLoader
import lib.mission
import lib.log

_config = ConfigLoader(syspath.cmd_folder + "/config")
_logger = lib.log.screenLog()

lib.mission.send_system_refreshinstalled(_config, _logger)
