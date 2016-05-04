#!/usr/bin/env python

from time import sleep
from daemonize import Daemonize
import schedule

from lib.configloader import ConfigLoader
import lib.mission
import lib.log

_config = ConfigLoader("config")
log = lib.log.Log(_config)
_logger = log.getLogger()
pid = _config.getPidFile()


def register():
    lib.mission.send_register(_config, _logger)


def updateinstalled():
    lib.mission.update_cache()
    lib.mission.send_system_updateinstalled(_config, _logger)


def system_notify():
    lib.mission.send_system_notify(_config, _logger)


def do_update():
    lib.mission.do_update(_config, _logger)

def main():
    if not _config.is_registered():
        register()
    updateinstalled()
    system_notify()
    do_update()
    schedule.every(2).hours.do(updateinstalled)
    schedule.every(10).minutes.do(system_notify)
    schedule.every(10).minutes.do(do_update)

    while True:
        schedule.run_pending()
        sleep(5)


#daemon = Daemonize(app="test_app", pid=pid, action=main, keep_fds=log.getKeepfds())
#daemon.start()
main()
