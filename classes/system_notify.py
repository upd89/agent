class System:

    def __init__(self, name, urn, os, address, reboot_required):
        self.name = name
        self.urn = urn
        self.os = os
        self.address = address
        self.rebootRequired = reboot_required
        self.updCount = 0
        self.packageUpdates = list()


    def increment(self):
        self.updCount += 1


    def addUpdate(self, update):
        self.packageUpdates.append(update)
        self.increment()
