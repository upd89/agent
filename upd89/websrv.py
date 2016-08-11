#!/usr/bin/env python

from lib.bottletlsdaemon import daemon_run
from bottle import get, post, request, run, abort, redirect
import json
import lib.persist


@get('/')
def index():
    return "nothing to see here"


@post('/task')
def new_task():
    cwd = os.environ.get['UPD89_DATADIR', '/etc/upd89']
    tasks = lib.persist.Persist(cwd + "/tasks.data")
    data = json.load(request.body)
    tasks.set_key(data.get('task_id').encode("utf8"), request.body.read())
    tasks.close()
    return("ok")


def start(config=None):
    if config == None:
        daemon_run(
            host     = '0.0.0.0',
            port     = os.environ["UPD89_WEBSRV_PORT"],
            pidfile  = os.environ["UPD89_WEBSRV_PIDFILE"],
            logfile  = os.environ["UPD89_WEBSRV_LOGFILE"],
            keyfile  = os.environ["UPD89_WEBSRV_KEYFILE"],
            certfile = os.environ["UPD89_WEBSRV_CERTFILE"],
            cafile   = os.environ["UPD89_WEBSRV_CAFILE"],
            action   = "start"
        )
    else:
        cpath = config.getTlsPath()
        daemon_run(
            host     = '0.0.0.0',
            port     = config.getWebserverPort(),
            pidfile  = config.getWebserverPidfile(),
            logfile  = config.getWebserverLogfile(),
            keyfile  = cpath + '/' + config.getTlsPrivKey(),
            certfile = cpath + '/' + config.getTlsPubCert(),
            cafile   = cpath + '/' + config.getTlsCa(),
            action   = "start"
        )


def stop(config=None):
    if config == None:
        daemon_run(
            pidfile = os.environ["UPD89_WEBSRV_PIDFILE"],
            action  = "stop"
        )
    else:
        daemon_run(
            pidfile = config.getWebserverPidfile(),
            action  = "stop"
        )


