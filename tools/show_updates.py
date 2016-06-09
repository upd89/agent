#!/usr/bin/env python

import apt

cache = apt.Cache()
cache.update()

for pkg in cache:
    if pkg.is_upgradable:
        print(pkg.name)
