#!/usr/bin/env python

from lib.configloader import ConfigLoader
import lib.mission
import lib.log

import sys
import os
import logging
import logging.handlers
from io import StringIO

logger = logging.getLogger(u'l')
logger.setLevel(logging.DEBUG)

mem_log = StringIO()
mem_log_handler = logging.StreamHandler(mem_log)
logger.addHandler(mem_log_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

_config = ConfigLoader("config")
_logger = lib.log.screenLog()

lib.mission.do_update(_config, _logger)
# logger.debug(unicode(os.getpid()))

print("---")
print(mem_log.getvalue())
