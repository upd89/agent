class System:

    def __init__(self, name, urn, os, address, reboot_required):
        self.name = name
        self.urn = urn
        self.os = os
        self.address = address
        self.reboot_required = reboot_required
        self.packageupdates = list()

    def addUpdate(self, update):
        self.packageupdates.append(update)
