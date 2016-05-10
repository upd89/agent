import os
import apt
import apt_pkg
import StringIO
from classes.update import Update
from classes.package import Package
from classes.packagelist import Packagelist
from classes.repository import Repository
from classes.package_version import PackageVersion
from classes.task_notify import TaskNotify

import logging


def updateCache():
    cache = apt.Cache()
    if os.geteuid() == 0:
        print("Updating cache...")
        try:
            cache.update()
        except:
            print("had some troubles, but anyway, let's go on...")
    cache.close()


def addUpdates(sys):
    print("Reading local cache...")
    cache = apt.Cache()
    print("Reading Upgradable Packages...")
    for pkg in cache:
        if (pkg.is_upgradable):
            pkg_base = pkg.versions[-1]
            pkg_origin = pkg.versions[0].origins[0]

            candidate_repo = Repository(archive=pkg_origin.archive,
                                        origin=pkg_origin.origin,
                                        component=pkg_origin.component)

            candidate_version = PackageVersion(version=pkg.candidate.version,
                                               sha256=pkg.candidate.sha256,
                                               arch=pkg.architecture(),
                                               repository=candidate_repo)

            update = Update(name=pkg.name,
                            candidate_version=candidate_version,
                            baseversion_hash=pkg_base.sha256)

            sys.addUpdate(update)
    cache.close()
    return sys


def getPackageList():
    cache = apt.Cache()
    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            pkg_origin = pkg.installed.origins[0]
            pkg_base = pkg.versions[-1]
            pkg_base_origin = pkg_base.origins[0]

            installed_repo = Repository(archive=pkg_origin.archive,
                                        origin=pkg_origin.origin,
                                        component=pkg_origin.component)

            installed_version = PackageVersion(version=pkg.installed.version,
                                               sha256=pkg.installed.sha256,
                                               arch=pkg.architecture(),
                                               repository=installed_repo)

            if (pkg.installed.sha256 == pkg_base.sha256):
                is_base_version = True
                base_version = False
            else:
                is_base_version = False
                base_repo = Repository(archive=pkg_base_origin.archive,
                                       origin=pkg_base_origin.origin,
                                       component=pkg_base_origin.component)
                base_version = PackageVersion(version=pkg_base.version,
                                              sha256=pkg_base.sha256,
                                              arch=pkg.architecture(),
                                              repository=base_repo)

            package = Package(name=pkg.name, section=pkg.section,
                              summary=pkg.installed.summary,
                              homepage=pkg.installed.homepage,
                              installed_version=installed_version,
                              is_base_version=is_base_version,
                              base_version=base_version)

            packages.add(package)
    cache.close()
    return packages


class PkgManager(apt_pkg.PackageManager):
    parent = apt_pkg.PackageManager
    depcache = apt_pkg.DepCache(apt_pkg.Cache())
    installation_plan = []

    def install(self, pkg, file):
        # print "Installing", pkg.get_fullname(True)
        self.installation_plan.append((pkg, u'Inst'))
        return True

    def configure(self, pkg):
        # print "Configuring", pkg.get_fullname(True)
        self.installation_plan.append((pkg, u'Conf'))
        return True

    def remove(self, pkg, purge):
        # print "Removing", pkg.get_fullname(True)
        self.installation_plan.append((pkg, u'Rem'))
        return True

    def go(self, fd):
        for (p, a) in self.installation_plan:
            if a == u'Inst' or a == u'Conf':
                ver = self.depcache.get_candidate_ver(p)
            else:
                ver = p.current_ver
            logger = logging.getLogger(u'l')
            logger.debug(
                a + u' ' + p.name + u' ' + ver.ver_str + u' ' + ver.arch)
        return True


def do_update(p_list):
    apt_pkg.PackageManager = PkgManager
    logger = logging.getLogger(u'l')
    output = StringIO.StringIO()
    cache = apt.Cache()
    for p in p_list:
        if p in cache:
            cache[p].mark_upgrade()
        else:
            logger.debug("package not found: " + p )

    # apt_pkg.config.set("APT::Get::Simulate", "true")
    # apt_pkg.config.set("dir::cache", "/tmp")
    result = cache.commit(install_progress=apt.progress.base.InstallProgress())
    if result:
        state = "Done"
    else:
        state = "Failed"
    cache.close()
    logger.debug(u"finished.")
    log = ""
    return(TaskNotify(state=state, log=log))
