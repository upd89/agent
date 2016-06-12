import json
import datetime
from upd89.lib import persist, upstream, sysinfo, pkg


def update_cache():
    pkg.updateCache()


def send_register(_config, _logger):
    sys = sysinfo.get_register_system()
    _logger.debug("Sending to server (register %s)..." %
                  sysinfo.get_hostname())
    response = upstream.pushRegister(_config, sys)
    _logger.debug("Response: " + response)
    _config.set_registered()


def send_system_refreshinstalled_hash(_config, _logger):
    known_packages = persist.Persist(_config.getDataDir() + "/known_packages.data")
    packages = pkg.getPackageHashList(known_packages.get_keys())
    _logger.debug("Sending to server (refreshInstalledHash %s)..." %
                  sysinfo.get_hostname())
    response = upstream.pushSystemRefreshInstalledHash(_config, sysinfo.get_urn(), packages)
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
        complete_packages = pkg.getPackageListIncremental(packages.packages)
        _logger.debug("Sending to server (refreshInstalled %s)..." %
                      sysinfo.get_hostname())
        response = upstream.pushSystemRefreshInstalled(_config, sysinfo.get_urn(), complete_packages)
        _logger.debug("Response: " + response)
        j = json.loads(response)

    # sending full list if we had a count mismatch
    if j.get("status") == "countMismatch":
        packages = pkg.getPackageHashList(list())
        _logger.debug("Sending to server (refreshInstalledHash after countMismatch %s)..." %
                       sysinfo.get_hostname())
        response = upstream.pushSystemRefreshInstalledHash(_config, sysinfo.get_urn(), packages)
        _logger.debug("Response: " + response)
        j = json.loads(response)
        print(j.get("status"))


def send_system_refreshinstalled(_config, _logger):
    packages = pkg.getPackageList()
    _logger.debug("Sending to server (refreshInstalled %s)..." %
                  sysinfo.get_hostname())
    response = upstream.pushSystemRefreshInstalled(_config, sysinfo.get_urn(), packages)
    _logger.debug("Response: " + response)


def send_system_notify_hash(_config, _logger):
    known_updates = persist.Persist(_config.getDataDir() + "/known_updates.data")
    sys = sysinfo.get_notify_system()
    sys = pkg.addUpdateHashes(sys, known_updates.get_keys())
    _logger.debug("Sending to server (notifyHash %s)..." %
                  sysinfo.get_hostname())
    response = upstream.pushSystemNotifyHash(_config, sysinfo.get_urn(), sys)
    _logger.debug("Response: " + response)

    j = json.loads(response)
    print j.get("status")
    for h in j.get("knownPackages"):
        now = datetime.datetime.now().strftime("%d.%m.%y %H:%M")
        known_updates.set_key(h.encode('ascii', 'ignore'), now)
        sys.packageUpdates.remove(h)
    print("unknown updates: %d" % len(sys.packageUpdates))
    known_updates.close() # update 'known updates' after this?

    # sending full information for unknown updates
    if (len(sys.packageUpdates) > 0):
        complete_sys = sysinfo.get_notify_system()
        complete_sys = pkg.addUpdatesIncremental(complete_sys, sys.packageUpdates)
        _logger.debug("Sending to server (notify %s)..." %
                      sysinfo.get_hostname())
        response = upstream.pushSystemNotify(_config, sysinfo.get_urn(), complete_sys)
        _logger.debug("Response: " + response)
        j = json.loads(response)

    # sending full list if we had a count mismatch
    if j.get("status") == "countMismatch":
        sys = sysinfo.get_notify_system()
        sys = pkg.addUpdateHashes(sys, list())
        _logger.debug("Sending to server (notifyHash after countMismatch %s)..." %
                      sysinfo.get_hostname())
        response = upstream.pushSystemNotifyHash(_config, sysinfo.get_urn(), sys)
        _logger.debug("Response: " + response)
        j = json.loads(response)
        print(j.get("status"))


def send_system_notify(_config, _logger):
    sys = sysinfo.get_notify_system()
    sys = pkg.addUpdates(sys)
    _logger.debug("Sending to server (notify %s)..." % sysinfo.get_hostname())
    response = upstream.pushSystemNotify(_config, sysinfo.get_urn(), sys)
    _logger.debug("Response: " + response)


def do_update(_config, _logger):
    tasks = persist.Persist(_config.getDataDir() + "/tasks.data")
    for key in tasks.get_keys():
        json_data = tasks.get_key(key)
        _logger.debug(u"key: %s - json: %s" % (key, json_data))
        t = json.loads(json_data)
        p_list = list()
        for p in t.get("packages"):
            pkg_name = p.get("pkg_name")
            pkg_version = p.get("pdk_version")
            p_list.append(pkg_name)
        tasknotify = pkg.do_update(p_list)
        response = upstream.pushTaskNotify(_config, key, tasknotify)
        _logger.debug("Response: " + response)
        tasks.delete_key(key)
    tasks.close()
