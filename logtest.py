#!/usr/bin/env python

import sys
import logging
import logging.handlers
from io import StringIO

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

mem_log = StringIO()
mem_log_handler = logging.StreamHandler(mem_log)
logger.addHandler(mem_log_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

print("test")

logger.debug(u'debug1')
logger.info(u'info2')
logger.debug(u'debug3')
logger.info(u'info4')

print("---")

print(mem_log.getvalue())

