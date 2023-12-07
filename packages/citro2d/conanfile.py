from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import copy, get
from conan.tools.scm import Version

import os

class Conan(ConanFile):
    name = 'citro2d'
    description = 'Library for drawing 2D graphics using the Nintendo 3DS\'s PICA200 GPU'
    url = 'https://github.com/devkitPro/citro2d'
    _source_subfolder = 'source_subfolder'

    settings = 'build_type'

    exports_sources = ["CMakeLists.txt"]
    generators = ["CMakeToolchain", "CMakeDeps"]

    tool_requires = ["dka_general_tools/[>=1.2.0]", "picasso/[>=2.7.0]"]

    def requirements(self):
        ver = Version(self.version)

        if ver <= Version("1.1.0"):
            self.requires('libctru/[<1.6.0]') # Upper bound due to changed font APIs
            self.requires('citro3d/[>=1.4.0 <1.6.1]') # Upper bound is the last version compatible with libctru <1.6.0
        elif ver <= Version("1.3.1"):
            self.requires('libctru/[>=1.6.0]') # Required for new font APIs since 1.2.0
            self.requires('citro3d/[>=1.4.0]')
        else:
            self.requires('libctru/[>=2.0.0]') # Required for new GSP_SCREEN_WIDTH definitions
            self.requires('citro3d/[>=1.4.0]')

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        os.rename("citro2d-%s" % self.version, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        vars = {}
        if Version(self.version) >= Version('1.2.0'):
            vars={'CITRO2D_NEWER_THAN_120':"ON"}
        cmake.configure(variables=vars)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        vars = {}
        if Version(self.version) >= Version('1.2.0'):
            vars={'CITRO2D_NEWER_THAN_120':"ON"}
        cmake.configure(variables=vars)
        cmake.install()
        copy(self, "*.h", os.path.join(self.source_folder, self._source_subfolder, "include"), os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.includedirs = [os.path.join(self.package_folder, "include")]
