from conan import ConanFile, tools
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = 'dka_3dstools'
    version = '1.1.4'
    url = 'https://github.com/devkitPro/3dstools'
    _source_subfolder = 'source_subfolder'

    settings = "build_type"

    exports_sources = ["CMakeLists.txt"]
    generators = "CMakeToolchain"

    def source(self):
        get(self, "https://github.com/devkitPro/3dstools/archive/v%s.tar.gz" % self.version, sha256='c68c53c87cf05faee1b5ed1e6ef49578faacca769e5be0a0b6fd7de4966f8d15')
        os.rename("3dstools-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.bindirs.append(os.path.join(self.package_folder, "bin"))
