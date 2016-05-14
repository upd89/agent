import os
import sys
import apt
import apt_pkg
from classes.update import Update
from classes.package import Package
from classes.packagelist import Packagelist
from classes.repository import Repository
from classes.package_version import PackageVersion
from classes.task_notify import TaskNotify


def _getCache():
    return apt.Cache(apt.progress.text.OpProgress())


def updateCache():
    cache = _getCache()
    if os.geteuid() == 0:
        print("Updating cache...")
        try:
            cache.update()
        except:
            print("had some troubles, but anyway, let's go on...")
    cache.close()


def addUpdateHashes(sys, knownHashes):
    print("Reading local cache...")
    cache = _getCache()
    print("Reading Upgradable Packages...")
    for pkg in cache:
        if (pkg.is_upgradable):
            if not pkg.candidate.sha256 in knownHashes:
                sys.addUpdate(pkg.candidate.sha256)
            else:
                sys.increment()
    cache.close()
    return sys


def addUpdates(sys):
    print("Reading local cache...")
    cache = _getCache()
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


def getPackageHashList(knownHashes):
    cache = _getCache()
    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            if not pkg.installed.sha256 in knownHashes:
                packages.add(pkg.installed.sha256)
            else:
                packages.increment()
    cache.close()
    return packages


def getPackageList():
    cache = _getCache()
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


def do_update(p_list):

    class TextInstallProgress(apt.progress.base.InstallProgress):

        def __init__(self, progress_log):
            self.progress_log = progress_log
            super(TextInstallProgress, self).__init__()

        def fork(self):
            pid = os.fork()
            if pid == 0:
                os.dup2(self.progress_log, 1)
                os.dup2(self.progress_log, 2)
            return pid

    apt_pkg.config.set("APT::Get::Simulate", "true")
    apt_pkg.config.set("dir::cache", "/tmp")
    cache = _getCache()
    state = "Failed"
    progress_output, progress_input = os.pipe()

    for p in p_list:
        if p in cache:
            cache[p].mark_upgrade()
        else:
            print("package not found: '%s'" % p)

    try:
        result = cache.commit(apt.progress.text.AcquireProgress(),
                              TextInstallProgress(progress_input))
        if result:
            state = "Done"
    except SystemError as e:
        print("Error while updating: '%s'" % e)
    cache.close()
    os.close(progress_input)
    log = os.fdopen(progress_output).read()
    print("---\n" + log + "\n---")
    return(TaskNotify(state=state, log=log))
