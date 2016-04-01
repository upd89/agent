class Package:
  def __init__(self, name, version, arch, baseversion, section, homepage, summary, repo):
    self.name = name
    self.version = version
    self.architecture = arch
    self.baseversion = baseversion
    self.section = section
    self.homepage = homepage
    self.summary = summary
    self.repository = repo

