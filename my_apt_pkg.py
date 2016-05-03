#!/usr/bin/env python

import apt_pkg
import sys
import apt


class PkgManager(apt_pkg.PackageManager):

    parent = apt_pkg.PackageManager
    depcache = apt_pkg.DepCache(apt_pkg.Cache())
    installionplan = []

    def install(self, pkg, file):
        # print "Installing", pkg.get_fullname(True)
        self.installionplan.append((pkg, "Inst"))
        return True

    def configure(self, pkg):
        # print "Configuring", pkg.get_fullname(True)
        self.installionplan.append((pkg, "Conf"))
        return True

    def remove(self, pkg, purge):
        # print "Removing", pkg.get_fullname(True)
        self.installionplan.append((pkg, "Rem"))
        return True

    def go(self, fd):
        for (p, a) in self.installionplan:
            if a == "Inst" or a == "Conf":
                ver = self.depcache.get_candidate_ver(p)
            else:
                ver = p.current_ver
            print a, p.name, ver.ver_str, ver.arch

        return True

apt_pkg.PackageManager = PkgManager


cache = apt.Cache()
pkg = cache["python"]
if pkg.is_installed:
    pkg.mark_delete()
else:
    pkg.mark_install()

apt_pkg.config.set("APT::Get::Simulate", "true")
apt_pkg.config.set("dir::cache", "/tmp")

print "COMMIT"
cache.commit(install_progress=apt.progress.base.InstallProgress())
