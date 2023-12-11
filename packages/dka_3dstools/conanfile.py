from conan import ConanFile, tools
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = 'dka_3dstools'
    url = 'https://github.com/devkitPro/3dstools'
    _source_subfolder = 'source_subfolder'

    settings = ['os', 'build_type']

    exports_sources = ["CMakeLists.txt"]
    generators = "CMakeToolchain"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
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
