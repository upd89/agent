class Packagelist:

    def __init__(self):
        self.pkgCount = 0
        self.packages = list()

    def add(self, package):
        self.packages.append(package)
        self.pkgCount += 1
