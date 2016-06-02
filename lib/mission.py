import json
import lib.persist
import lib.upstream
import lib.sysinfo
import lib.pkg
import datetime


def update_cache():
    lib.pkg.updateCache()


def send_register(_config, _logger):
    sys = lib.sysinfo.get_register_system()
    _logger.debug("Sending to server (register %s)..." %
                  lib.sysinfo.get_hostname())
    response = lib.upstream.pushRegister(_config, sys)
    _logger.debug("Response: " + response)
    _config.set_registered()


def send_system_refreshinstalled_hash(_config, _logger):
    known_packages = lib.persist.Persist("/opt/upd89/agent/known_packages.data")
    packages = lib.pkg.getPackageHashList(known_packages.get_keys())
    _logger.debug("Sending to server (refreshInstalledHash %s)..." %
                  lib.sysinfo.get_hostname())
    response = lib.upstream.pushSystemRefreshInstalledHash(_config, lib.sysinfo.get_urn(), packages)
    _logger.debug("Response: " + response)

    j = json.loads(response)
    print j.get("status")
    for h in j.get("knownPackages"):
        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        known_packages.set_key(h.encode('ascii', 'ignore'), now)
        packages.packages.remove(h)
    print("unknown packages: %d" % len(packages.packages))
    known_packages.close() # update 'known packages' after this?

    # sending full information for unknown packages
    if (len(packages.packages) > 0):
        complete_packages = lib.pkg.getPackageListIncremental(packages.packages)
        _logger.debug("Sending to server (refreshInstalled %s)..." %
                      lib.sysinfo.get_hostname())
        response = lib.upstream.pushSystemRefreshInstalled(_config, lib.sysinfo.get_urn(), complete_packages)
        _logger.debug("Response: " + response)
        j = json.loads(response)

    # sending full list if we had a count mismatch
    if j.get("status") == "countMismatch":
        packages = lib.pkg.getPackageHashList(list())
        _logger.debug("Sending to server (refreshInstalledHash after countMismatch %s)..." %
                       lib.sysinfo.get_hostname())
        response = lib.upstream.pushSystemRefreshInstalledHash(_config, lib.sysinfo.get_urn(), packages)
        _logger.debug("Response: " + response)
        j = json.loads(response)
        print(j.get("status"))


def send_system_refreshinstalled(_config, _logger):
    packages = lib.pkg.getPackageList()
    _logger.debug("Sending to server (refreshInstalled %s)..." %
                  lib.sysinfo.get_hostname())
    response = lib.upstream.pushSystemRefreshInstalled(_config, lib.sysinfo.get_urn(), packages)
    _logger.debug("Response: " + response)


def send_system_notify_hash(_config, _logger):
    known_updates = lib.persist.Persist("/opt/upd89/agent/known_updates.data")
    sys = lib.sysinfo.get_notify_system()
    sys = lib.pkg.addUpdateHashes(sys, known_updates.get_keys())
    _logger.debug("Sending to server (notifyHash %s)..." %
                  lib.sysinfo.get_hostname())
    response = lib.upstream.pushSystemNotifyHash(_config, lib.sysinfo.get_urn(), sys)
    _logger.debug("Response: " + response)

    j = json.loads(response)
    print j.get("status")
    for h in j.get("knownPackages"):
        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        known_updates.set_key(h.encode('ascii', 'ignore'), now)
        sys.packageUpdates.remove(h)
    print("unknown updates: %d" % len(sys.packageUpdates))
    known_packages.close() # update 'known updates' after this?

    # sending full information for unknown updates
    if (len(sys.packageUpdates) > 0):
        complete_sys = lib.sysinfo.get_notify_system()
        complete_sys = lib.pkg.addUpdatesIncremental(complete_sys, sys.packageUpdates)
        _logger.debug("Sending to server (notify %s)..." %
                      lib.sysinfo.get_hostname())
        response = lib.upstream.pushSystemNotify(_config, lib.sysinfo.get_urn(), complete_sys)
        _logger.debug("Response: " + response)
        j = json.loads(response)

    # sending full list if we had a count mismatch
    if j.get("status") == "countMismatch":
        sys = lib.sysinfo.get_notify_system()
        sys = lib.pkg.addUpdateHashes(sys, list())
        _logger.debug("Sending to server (notifyHash after countMismatch %s)..." %
                      lib.sysinfo.get_hostname())
        response = lib.upstream.pushSystemNotifyHash(_config, lib.sysinfo.get_urn(), sys)
        _logger.debug("Response: " + response)
        j = json.loads(response)
        print(j.get("status"))


def send_system_notify(_config, _logger):
    sys = lib.sysinfo.get_notify_system()
    sys = lib.pkg.addUpdates(sys)
    _logger.debug("Sending to server (notify %s)..." % lib.sysinfo.get_hostname())
    response = lib.upstream.pushSystemNotify(_config, lib.sysinfo.get_urn(), sys)
    _logger.debug("Response: " + response)


def do_update(_config, _logger):
    tasks = lib.persist.Persist("/opt/upd89/agent/tasks.data")
    for key in tasks.get_keys():
        json_data = tasks.get_key(key)
        _logger.debug(u"key: %s - json: %s" % (key, json_data))
        t = json.loads(json_data)
        p_list = list()
        for p in t.get("packages"):
            pkg_name = p.get("pkg_name")
            pkg_version = p.get("pdk_version")
            p_list.append(pkg_name)
        tasknotify = lib.pkg.do_update(p_list)
        response = lib.upstream.pushTaskNotify(_config, key, tasknotify)
        _logger.debug("Response: " + response)
        tasks.delete_key(key)
    tasks.close()
