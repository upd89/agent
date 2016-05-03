class Package:

    def __init__(self, name, section, summary, homepage, installed_version,
                 is_base_version, base_version):
        self.name = name
        self.section = section
        self.summary = summary
        self.homepage = homepage
        self.installedVersion = installed_version
        self.isBaseVersion = is_base_version
        self.baseVersion = base_version

