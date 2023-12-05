from conan import ConanFile, tools
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = 'picasso'
    version = '2.7.0'
    url = 'https://github.com/fincs/picasso'
    description = 'Homebrew PICA200 shader assembler'
    _source_subfolder = 'source_subfolder'

    settings = "build_type"

    exports_sources = ["CMakeLists.txt"]
    generators = "CMakeToolchain"

    def source(self):
        get(self, "https://github.com/fincs/picasso/archive/v%s.tar.gz" % self.version, sha256='9f4fe929031fd11219fb93d1cb5c51ba65feaa09d0aacad9b84662f9c3f1572f')
        os.rename("picasso-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={'PACKAGE_STRING':"picasso %s" % self.version})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(variables={'PACKAGE_STRING':"picasso %s" % self.version})
        cmake.install()

    def package_info(self):
        self.cpp_info.bindirs.append(os.path.join(self.package_folder, "bin"))
