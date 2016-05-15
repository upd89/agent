#!/usr/bin/env python

from lib.bottletlsdaemon import daemon_run
from bottle import get, post, request, run, abort, redirect
import json
import lib.persist
import lib.sysinfo
from lib.configloader import ConfigLoader

_config = ConfigLoader("websrv.ini")
port = _config.getWebserverPort()
logfile = _config.getWebserverLogfile()
pidfile = _config.getWebserverPidfile()

import os
cwd = os.getcwd()


@get('/')
def index():
    return "nothing to see here"


@post('/task')
def new_task():
    tasks = lib.persist.Persist(cwd + "/tasks.data")
    # TODO: Test if json is valid
    data = json.load(request.body)
    tasks.set_key(data.get('task_id').encode("utf8"), request.body.read())
    tasks.close()
    return("ok")


if __name__ == "__main__":
    my_ip = lib.sysinfo.get_ip()
    capath = _config.getTlsPath()
    key_file = capath + '/' + _config.getTlsPrivKey()
    cert_file = capath + '/' + _config.getTlsPubCert()
    ca_file = capath + '/' + _config.getTlsCa()
    daemon_run(host=my_ip, port=port, pidfile=pidfile, logfile=logfile,
               key_file=key_file, cert_file=cert_file, ca_file=ca_file)
