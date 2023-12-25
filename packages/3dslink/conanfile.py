from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = '3dslink'
    url = 'https://github.com/devkitPro/tex3ds'
    description = 'Wi-Fi code upload tool for quick and easy testing of 3DS homebrew'
    _source_subfolder = 'source_subfolder'

    settings = ['os', 'arch', 'compiler', 'build_type']

    exports_sources = ['CMakeLists.txt']
    generators = ['CMakeToolchain', 'CMakeDeps']
    requires = ['zlib/[>=1.2.0]']

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        os.rename("3dslink-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(variables={'PACKAGE_STRING':"3dslink %s" % self.version})
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending to PATH: " + bindir)
        self.env_info.PATH.append(bindir)
