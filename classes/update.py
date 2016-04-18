class Update:

    def __init__(self, name, version, arch, repository, baseversion, sha256):
        self.name = name
        self.version = version
        self.architecture = arch
        self.repository = repository
        self.baseversion = baseversion
        self.sha256 = sha256
