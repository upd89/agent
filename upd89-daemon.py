#!/usr/bin/env python

import sys
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


def refreshinstalled():
    # lib.mission.send_system_refreshinstalled(_config, _logger)
    lib.mission.send_system_refreshinstalled_hash(_config, _logger)


def system_notify():
    lib.mission.update_cache()
    # lib.mission.send_system_notify(_config, _logger)
    lib.mission.send_system_notify_hash(_config, _logger)


def do_update():
    #_logger.debug("Checking for new Tasks...")
    lib.mission.do_update(_config, _logger)


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


if '-h' in sys.argv:
    print("\n '--no-daemonize' do not run in background\n")
    sys.exit()

from subprocess import call
call(["/usr/bin/env", "python", "upd89-websrv.py", "start"])

if '--no-daemonize' in sys.argv:
    main()
else:
    daemon = Daemonize(app="test_app", pid=pid,
                       action=main, keep_fds=log.getKeepfds())
    daemon.start()
