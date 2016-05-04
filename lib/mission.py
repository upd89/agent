import json
import lib.persist
import lib.upstream
import lib.sysinfo
import lib.pkg


def update_cache():
    lib.pkg.updateCache()


def send_register(_config, _logger):
    sys = lib.sysinfo.get_register_system()
    _logger.debug(
        "Sending to server (register " + lib.sysinfo.get_hostname() + ")...")
    response = lib.upstream.pushRegister(_config, sys)
    _logger.debug("Response:\n" + response)
    _config.set_registered()


def send_system_updateinstalled(_config, _logger):
    packages = lib.pkg.getPackageList()
    _logger.debug(
        "Sending to server (updateInstalled " + lib.sysinfo.get_hostname() + ")...")
    response = lib.upstream.pushSystemUpdateInstalled(
        _config, lib.sysinfo.get_urn(), packages)
    _logger.debug("Response:\n" + response)


def send_system_notify(_config, _logger):
    sys = lib.sysinfo.get_notify_system()
    sys = lib.pkg.addUpdates(sys)
    _logger.debug(
        "Sending to server (notify " + lib.sysinfo.get_hostname() + ")...")
    response = lib.upstream.pushSystemNotify(
        _config, lib.sysinfo.get_urn(), sys)
    _logger.debug("Response:\n" + response)


def do_update(_config, _logger):
    tasks = lib.persist.Persist("tasks.data")
    for key in tasks.get_keys():
        json_data = tasks.get_key(key)
        _logger.debug("key: " + key +" - json: " + json_data)
        t = json.loads(json_data)
        p_list = list()
        for p in t.get("packages"):
            pkg_name = p.get("pkg_name")
            pkg_version = p.get("pdk_version")
            p_list.append(pkg_name)
        tasknotify = lib.pkg.do_update(p_list)
        response = lib.upstream.pushTaskNotify(_config, key, tasknotify)
        _logger.debug("Response:\n" + response)
        tasks.delete_key(key)

