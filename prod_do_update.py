#!/usr/bin/env python

from lib.configloader import ConfigLoader
import lib.mission
import lib.log

_config = ConfigLoader("config")
_logger = lib.log.screenLog()

lib.mission.do_update(_config, _logger)
