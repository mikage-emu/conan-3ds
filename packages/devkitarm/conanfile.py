from conan import ConanFile
from conan.tools.files import chdir, copy, get, rename
from conan.tools.cmake import cmake_layout

from conan.tools.scm import Git

import os

class Conan(ConanFile):
    name = 'devkitarm'
    description = 'A port of the GNU Compiler Collection (GCC)'
    url = 'https://github.com/devkitPro'

    exports_sources = 'DevkitArm3DS.cmake'

    # NOTE: devkitarm-rules requires dka_general_tools >= 1.3.0 at some point due to using generate_compile_commands
    #def requirements(self):
    #    if int(self.version) >= TODO: # TODO: Version r53 (maybe already r50) require https://github.com/devkitPro/devkitarm-rules
    #        self.requires('dka_general_tools/[>=1.3.0]')

    def build(self):
        get(self, **self.conan_data["sources"][self.version])
        if int(self.version) >= 48:
            rename(self, "opt/devkitpro/devkitARM", "devkitARM")

        if int(self.version) >= 53: # TODO: Version r53 (maybe already r50) require https://github.com/devkitPro/devkitarm-rules
            git = Git(self, ".")
            git.clone("https://github.com/devkitPro/devkitarm-rules")
            with chdir(self, "devkitarm-rules"):
                git.checkout("v1.0.0");
            copy(self, "*", "devkitarm-rules", "devkitARM")

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
