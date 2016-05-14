#!/usr/bin/env python

from lib.configloader import ConfigLoader
import lib.mission
import lib.log

_config = ConfigLoader("config")
_logger = lib.log.screenLog()

lib.mission.send_system_notify_hash(_config, _logger)
