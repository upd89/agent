#!/usr/bin/env python

import syspath
from upd89.lib.configloader import ConfigLoader
import upd89.lib.mission
import upd89.lib.log

_config = ConfigLoader(syspath.cmd_folder + "/config")
_logger = upd89.lib.log.screenLog()

upd89.lib.mission.send_system_notify_hash(_config, _logger)
