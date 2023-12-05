from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = 'dka_general_tools'
    version = '1.2.0'
    url = 'https://github.com/devkitPro/general-tools'
    _source_subfolder = 'source_subfolder'

    settings = "build_type"

    exports_sources = ["CMakeLists.txt"]
    generators = "CMakeToolchain"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        os.rename("general-tools-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={'PACKAGE_STRING':"dka-tools %s" % self.version})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(variables={'PACKAGE_STRING':"dka-tools %s" % self.version})
        cmake.install()

    def package_info(self):
        self.cpp_info.bindirs.append(os.path.join(self.package_folder, "bin"))
