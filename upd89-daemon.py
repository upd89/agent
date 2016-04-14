#!/usr/bin/env python

from time import sleep
from daemonize import Daemonize
import schedule

from lib.configloader.configloader import ConfigLoader
import lib.log.log
import lib.upstream
import lib.sysinfo
import lib.apt

_config = ConfigLoader("config")
log = lib.log.log.Log(_config)
logger = log.getLogger()
pid = _config.getPidFile()


def sendSystemNotify():
    logger.debug("Job is working")
    sys = lib.sysinfo.get_notify_system()
    sys = lib.apt.addUpdates(sys)
    logger.debug("Sending to server (notify " + lib.sysinfo.get_hostname() + ")...")
    response = lib.upstream.pushSystemNotify(_config, lib.sysinfo.get_urn(), sys)
    logger.debug("Response:\n" + response)


def main():
    schedule.every(5).minutes.do(sendSystemNotify)

    while True:
        schedule.run_pending()
        sleep(5)


daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=log.getKeepfds())
daemon.start()
