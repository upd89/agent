import os
os.putenv("DEBIAN_FRONTEND", "noninteractive")
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

def _getBaseSha256(pkg):
    pkg_base = pkg.versions[-1]
    if (pkg_base.sha256 == ''):
        pkg_arch = pkg.architecture()
        return "no_hash_for_" + pkg.name + '_' + pkg_arch + '_' + pkg_base.version
    else:
        return pkg_base.sha256

def _getInstalledSha256(pkg):
    if (pkg.installed.sha256 == ''):
        pkg_arch = pkg.architecture()
        return "no_hash_for_" + pkg.name + '_' + pkg_arch + '_' + pkg.installed.version
    else:
        return pkg.installed.sha256

def _getCandidateSha256(pkg):
    if (pkg.candidate.sha256 == ''):
        pkg_arch = pkg.architecture()
        return "no_hash_for_" + pkg.name + '_' + pkg_arch + '_' + pkg.candidate.version
    else:
        return pkg.candidate.sha256

def _buildPackage(pkg):
    pkg_origin = pkg.installed.origins[0]
    pkg_base = pkg.versions[-1]
    pkg_base_origin = pkg_base.origins[0]
    pkg_arch = pkg.architecture()

    inst_sha256 = _getInstalledSha256(pkg)
    base_sha256 = _getBaseSha256(pkg)

    installed_repo = Repository(archive=pkg_origin.archive,
                                origin=pkg_origin.origin,
                                component=pkg_origin.component)

    installed_version = PackageVersion(version=pkg.installed.version,
                                       sha256=inst_sha256,
                                       arch=pkg_arch,
                                       repository=installed_repo)


    if (base_sha256 == inst_sha256):
        is_base_version = True
        base_version = False
    else:
        is_base_version = False
        base_repo = Repository(archive=pkg_base_origin.archive,
                               origin=pkg_base_origin.origin,
                               component=pkg_base_origin.component)

        base_version = PackageVersion(version=pkg_base.version,
                                      sha256=base_sha256,
                                      arch=pkg_arch,
                                      repository=base_repo)

    package = Package(name=pkg.name, section=pkg.section,
                      summary=pkg.installed.summary,
                      homepage=pkg.installed.homepage,
                      installed_version=installed_version,
                      is_base_version=is_base_version,
                      base_version=base_version)

    return package


def _buildUpdate(pkg):
    pkg_base = pkg.versions[-1]
    pkg_origin = pkg.versions[0].origins[0]
    pkg_arch = pkg.architecture()

    upd_sha256 = _getCandidateSha256(pkg)
    base_sha256 = _getBaseSha256(pkg)

    candidate_repo = Repository(archive=pkg_origin.archive,
                                origin=pkg_origin.origin,
                                component=pkg_origin.component)

    candidate_version = PackageVersion(version=pkg.candidate.version,
                                       sha256=upd_sha256,
                                       arch=pkg_arch,
                                       repository=candidate_repo)

    update = Update(name=pkg.name,
                    candidate_version=candidate_version,
                    baseversion_hash=base_sha256)

    return update


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
            upd_sha256 = _getCandidateSha256(pkg)
            if not upd_sha256 in knownHashes:
                sys.addUpdate(upd_sha256)
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
            sys.addUpdate(_buildUpdate(pkg))
    cache.close()
    return sys


def addUpdatesIncremental(sys, requestedPackages):
    print("Reading local cache...")
    cache = _getCache()
    print("Reading Upgradable Packages...")
    for pkg in cache:
        if (pkg.is_upgradable):
            upd_sha256 = _getCandidateSha256(pkg)
            if (upd_sha256 in requestedPackages):
                sys.addUpdate(_buildUpdate(pkg))
            else:
                sys.increment()
    cache.close()
    return sys


def getPackageHashList(knownHashes):
    cache = _getCache()
    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            inst_sha256 = _getInstalledSha256(pkg)
            if not inst_sha256 in knownHashes:
                packages.add(inst_sha256)
            else:
                packages.increment()
    cache.close()
    return packages


def getPackageList():
    cache = _getCache()
    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            packages.add(_buildPackage(pkg))
    cache.close()
    return packages


def getPackageListIncremental(requestedPackages):
    cache = _getCache()
    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            inst_sha256 = _getInstalledSha256(pkg)
            if (inst_sha256 in requestedPackages):
                packages.add(_buildPackage(pkg))
            else:
                packages.increment()
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
