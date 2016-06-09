#!/usr/bin/env python

import syspath
from lib.configloader import ConfigLoader
import lib.log

import sys
import os
import logging
import logging.handlers
from StringIO import StringIO


class RedirectStdStreams(object):

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

_config = ConfigLoader(syspath.cmd_folder + "/config")
_logger = lib.log.screenLog()

mem_log = StringIO()

with RedirectStdStreams(stdout=mem_log, stderr=mem_log):
    print("RedirectStdStream...")
    import lib.mission
    lib.mission.do_update(_config, _logger)

print("--")
print(mem_log.getvalue())
