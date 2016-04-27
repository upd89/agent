#!/usr/bin/env python

from bottledaemon import daemon_run
from bottle import get, post, request, run, abort, redirect
import json
import lib.persist
import lib.sysinfo

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
    daemon_run(host=my_ip, port=8080, pidfile = cwd + "/websrv.pid",
               logfile = cwd + "/websrv.log")
