import os
import apt
from classes.update import Update
from classes.package import Package
from classes.packagelist import Packagelist


def addUpdates(sys):

    print("Reading local cache...")
    cache = apt.Cache()

    if os.geteuid() == 0:
        print("Updating cache...")
        try:
            cache.update()
        except:
            print("had some troubles, but anyway, let's go on...")

    print("Reading Upgradable Packages...")
    for pkg in cache:
        if (pkg.is_upgradable):
            # print(pkg.name)
            pkg_base = pkg.versions[-1]
            pkg_origin = pkg.versions[0].origins[0]
            repo_string = pkg_origin.origin + "_" + \
                pkg_origin.archive + "_" + pkg_origin.component
            sys.addUpdate(Update(
                name=pkg.name,
                version=pkg.candidate.version,
                arch=pkg.architecture(),
                repository=repo_string,
                baseversion=pkg_base.version
            ))

    return sys


def getPackageList():

    print("Reading local cache...")
    cache = apt.Cache()

    packages = Packagelist()
    for pkg in cache:
        if (pkg.is_installed):
            pkg_base = pkg.versions[-1]
            pkg_origin = pkg_base.origins[0]
            repo_string = pkg_origin.origin + "_" + \
                pkg_origin.archive + "_" + pkg_origin.component
            packages.add(Package(
                name=pkg.name,
                version=pkg.installed.version,
                arch=pkg.architecture(),
                baseversion=pkg_base.version,
                section=pkg.section,
                homepage=pkg.installed.homepage,
                summary=pkg.installed.summary,
                repo=repo_string
            ))

    return packages
