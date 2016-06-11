#!/usr/bin/env python

import os
import sys
import argparse
from time import sleep
from daemonize import Daemonize
import schedule

from lib.configloader import ConfigLoader
from lib import mission
import lib.log


def _load_config(configfile):
    global _config, _log, _logger, _pid
    _config = ConfigLoader(configfile)
    _log = lib.log.Log(_config)
    _logger = _log.getLogger()
    _pid = _config.getPidFile()


def register():
    mission.send_register(_config, _logger)


def refreshinstalled():
    # mission.send_system_refreshinstalled(_config, _logger)
    mission.send_system_refreshinstalled_hash(_config, _logger)


def system_notify():
    mission.update_cache()
    # mission.send_system_notify(_config, _logger)
    mission.send_system_notify_hash(_config, _logger)


def do_update():
    #_logger.debug("Checking for new Tasks...")
    mission.do_update(_config, _logger)


def main():
    if not _config.is_registered():
        register()
    refreshinstalled()
    system_notify()
    schedule.every(2).hours.do(refreshinstalled)
    schedule.every(10).minutes.do(system_notify)
    schedule.every(30).seconds.do(do_update)

    while True:
        schedule.run_pending()
        sleep(5)


def start(configfile):
    _load_config(configfile)

    newpid = os.fork()
    if newpid == 0:
        import websrv
        websrv.start(_config)
    else:
        daemon = Daemonize(app="test_app", pid=_pid, action=main,
                           keep_fds=_log.getKeepfds())
        daemon.start()


def stop(configfile):
    _load_config(configfile)

    import websrv
    websrv.stop(_config)

    with open(_pid, "r") as p:
        pid = int(p.read())
        os.kill(pid, signal.SIGTERM)


def debug(configfile):
    _load_config(configfile)
    main()

