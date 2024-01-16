from conan import ConanFile, tools
from conan.tools.files import chdir, copy, get
from conan.tools.gnu import Autotools

import os

class Conan(ConanFile):
    name = 'ctrtool'
    settings = ['os', 'arch', 'compiler', 'build_type']
    description = 'General purpose reading/extraction tool for Nintendo 3DS file formats'
    url = 'https://github.com/3DSGuy/Project_CTR/tree/master/ctrtool'

    generators = "AutotoolsToolchain"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        with chdir(self, os.path.join(self.source_folder, 'ctrtool')):
            autotools = Autotools(self)
            autotools.make(target='deps')
            autotools.make()

    def package(self):
        copy(self, "bin/*", src=os.path.join(self.source_folder, 'ctrtool'), dst=self.package_folder)

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending to PATH: " + bindir)
        self.env_info.PATH.append(bindir)
