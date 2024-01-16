from conan import ConanFile, tools
from conan.tools.files import chdir, copy, get
from conan.tools.gnu import Autotools

import os

class Conan(ConanFile):
    name = 'makerom'
    settings = ['os', 'arch', 'compiler', 'build_type']
    description = 'A CLI tool to create Nintendo 3DS ROM images'
    url = 'https://github.com/3DSGuy/Project_CTR/tree/master/makerom'

    generators = "AutotoolsToolchain"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        with chdir(self, os.path.join(self.source_folder, 'makerom')):
            autotools = Autotools(self)
            autotools.make(target='deps')
            autotools.make()

    def package(self):
        copy(self, "bin/*", src=os.path.join(self.source_folder, 'makerom'), dst=self.package_folder)

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending to PATH: " + bindir)
        self.env_info.PATH.append(bindir)
