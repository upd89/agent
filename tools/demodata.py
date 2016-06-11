from upd89.classes.system_register import System as RegisterSystem
from upd89.classes.system_notify import System as NotifySystem
from upd89.classes.update import Update
from upd89.classes.package_version import PackageVersion
from upd89.classes.repository import Repository
from upd89.classes.packagelist import Packagelist
from upd89.classes.package import Package


hostname = "demo-vm"
address = "127.0.0.1:8080"
distro = "demo-vm"

pkg1 = 'demo-vim'
summary1 = 'summary for demo-vim'
b_ver1 = 'demo-1.00'
i_ver1 = 'demo-1.01ubuntu2'
c_ver1 = 'demo-1.01ubuntu3'
b_sha256_1 = '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'
i_sha256_1 = 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35'
c_sha256_1 = '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce'

pkg2 = 'demo-dnsutils'
summary2 = 'summary for demo-dnsutils'
b_ver2 = 'demo-1.1'
c_ver2 = 'demo-1.1f'
b_sha256_2 = '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'
c_sha256_2 = 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d'

arch = "amd64"
section = "demo"
homepage = "http://upd89.org"
repo = Repository(origin='Ubuntu', archive='wily', component='main')
upd_repo = Repository(
    origin='Ubuntu', archive='wily-updates', component='main')


# system register

register_sys = RegisterSystem(hostname, hostname, distro, address, "")


# system refreshInstalled

packages = Packagelist()

installed_version1 = PackageVersion(
    version=i_ver1, sha256=i_sha256_1, arch=arch, repository=upd_repo)
base_version1 = PackageVersion(
    version=b_ver1, sha256=b_sha256_1, arch=arch, repository=repo)
package1 = Package(name=pkg1, section=section, summary=summary1,
                   homepage=homepage, installed_version=installed_version1,
                   is_base_version=False, base_version=base_version1)
packages.add(package1)

installed_version2 = PackageVersion(
    version=b_ver2, sha256=b_sha256_2, arch=arch, repository=repo)
package2 = Package(name=pkg2, section=section, summary=summary2,
                   homepage=homepage, installed_version=installed_version2,
                   is_base_version=True, base_version=False)
packages.add(package2)


# system notify

notify_sys = NotifySystem(hostname, hostname, distro, address, True)

candidate_version1 = PackageVersion(version=c_ver1, sha256=c_sha256_1,
                                    arch=arch, repository=upd_repo)
update1 = Update(name=pkg1, candidate_version=candidate_version1,
                 baseversion_hash=b_sha256_1)
notify_sys.addUpdate(update1)

candidate_version2 = PackageVersion(version=c_ver2, sha256=c_sha256_2,
                                    arch=arch, repository=upd_repo)
update2 = Update(name=pkg2, candidate_version=candidate_version2,
                 baseversion_hash=b_sha256_2)
notify_sys.addUpdate(update2)
