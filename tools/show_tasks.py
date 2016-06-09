#!/usr/bin/env python

import syspath
import json
import lib.persist

tasks = lib.persist.Persist(syspath.cmd_folder + "tasks.data")

for key in tasks.get_keys():
    print key
    print tasks.get_key(key)

tasks.close()
