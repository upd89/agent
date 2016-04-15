import os
import platform
import socket

import classes.system_register
import classes.system_notify


def get_hostname():
    return socket.gethostname()


def get_urn():
    return 'demo-' + get_hostname() + '-demo'


def get_distro():
    return ' '.join(platform.linux_distribution())


def get_reboot_required():
    return os.path.isfile("/var/run/reboot-required")


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

    # also possible:
    # my_ip = load(urlopen('http://jsonip.com'))['ip']


def get_register_system():
    myHostname = get_hostname()
    myURN = get_urn()
    myDistro = get_distro()
    myIP = get_ip()
    return classes.system_register.System(name=myHostname, urn=myURN,
                                          os=myDistro, address=myIP, tag="")


def get_notify_system():
    myHostname = get_hostname()
    myURN = get_urn()
    myDistro = get_distro()
    myIP = get_ip()
    needReboot = get_reboot_required()
    return classes.system_notify.System(name=myHostname, urn=myURN,
                                        os=myDistro, address=myIP,
                                        reboot_required=needReboot)
