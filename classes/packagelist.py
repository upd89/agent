class Packagelist:

    def __init__(self):
        self.pkgCount = 0
        self.packages = list()


    def increment(self):
        self.pkgCount += 1


    def add(self, package):
        self.packages.append(package)
        self.increment()
