from conan import ConanFile
from conan.tools.files import copy, get, rename
from conan.tools.cmake import cmake_layout

import os

class Conan(ConanFile):
    name = 'devkitarm'
    description = 'A port of the GNU Compiler Collection (GCC)'
    url = 'https://github.com/devkitPro'

    exports_sources = 'DevkitArm3DS.cmake'

    def build(self):
        get(self, **self.conan_data["sources"][self.version])
        if int(self.version) >= 48:
            rename(self, "opt/devkitpro/devkitARM", "devkitARM")

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", [os.path.join(self.package_folder, "DevkitArm3DS.cmake")])
        self.conf_info.define("user.devkitarm.version", self.version)

        toolchain_path = os.path.join(self.package_folder, "devkitARM")

        bindir = os.path.join(toolchain_path, "bin")
        self.output.info("Appending to PATH: " + bindir)
        self.cpp_info.bindirs = [bindir]

        self.buildenv_info.define("CC",  os.path.join(bindir, "arm-none-eabi-gcc")) # TODO: -cc instead of -gcc?
        self.buildenv_info.define("CXX", os.path.join(bindir, "arm-none-eabi-g++"))
        self.buildenv_info.define("DEVKITARM", toolchain_path)

        # TODO: Add newlib libs and headers

        # TODO: Add binutils path. Arm-non-eabi-as
        #self.env_info.PATH.append(os.path.join(toolchain_path, "bin/gcc/arm-none-eabi/"))
