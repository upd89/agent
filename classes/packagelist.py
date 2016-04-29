class Packagelist:

    def __init__(self):
        self.packages = list()
        self.pkgCount = 0

    def add(self, package):
        self.packages.append(package)
        self.pkgCount =+ 1
