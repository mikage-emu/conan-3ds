from conan import ConanFile
from conan.tools.files import copy, mkdir

import os

class Recipe(ConanFile):
    name = "dka_pkgconf"
    version = "2.1.0"
    description = "Wrapper around pkgconf to replace arm-none-eabi-pkg-config"

    exports_sources = "arm-none-eabi-pkg-config"

    requires = 'pkgconf/2.1.0'

    def package(self):
        copy(self, "arm-none-eabi-pkg-config", src=self.source_folder, dst=os.path.join(self.package_folder, "bin"))
