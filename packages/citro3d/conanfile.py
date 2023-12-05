from conan import ConanFile, tools
from conan.tools.files import chdir, collect_libs, copy, get, replace_in_file
from conan.tools.gnu import Autotools

import os

class Conan(ConanFile):
    name = 'citro3d'
    version = '1.5.0'
    settings = 'compiler', 'build_type'
    description = 'Homebrew PICA200 GPU wrapper library for Nintendo 3DS'
    url = 'https://github.com/fincs/citro3d'

    requires = 'libctru/1.5.1'
    exports_sources = 'add_missing_includes.patch'

    generators = "AutotoolsToolchain"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        #tools.patch(base_path=".", patch_file="add_missing_includes.patch")

    def build(self):
        with chdir(self, self.source_folder):
            autotools = Autotools(self)
            autotools.make()

    def package(self):
        copy(self, "*", src=self.source_folder, dst=self.package_folder)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
