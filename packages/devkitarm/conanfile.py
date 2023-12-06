from conan import ConanFile
from conan.tools.files import chdir, copy, download, get, rename, replace_in_file, unzip
from conan.tools.cmake import cmake_layout
from conan.tools.gnu import Autotools, AutotoolsToolchain

from conan.tools.scm import Git

from conans.util.runners import check_output_runner

import os

class Conan(ConanFile):
    name = 'devkitarm'
    description = 'A port of the GNU Compiler Collection (GCC)'
    url = 'https://github.com/devkitPro'

    exports_sources = 'DevkitArm3DS.cmake'

    # NOTE: devkitarm-rules requires dka_general_tools >= 1.3.0 at some point due to using generate_compile_commands
    #def requirements(self):
    #    if int(self.version) >= TODO: # TODO: Version r51 require https://github.com/devkitPro/devkitarm-rules
    #        self.requires('dka_general_tools/[>=1.3.0]')

    def generate(self):
        autotools = AutotoolsToolchain(self)
        env = autotools.environment()
        env.define("DEVKITPRO", self.build_folder)
        env.define("DEVKITARM", os.path.join(self.build_folder, "devkitARM"))
        autotools.generate(env)

    def build_requirements(self):
        if (self.conan_data["sources"][self.version]["url"].endswith("zst")):
            #if int(self.version) >= 60:
            self.tool_requires('zstd/[>=1.3.0]')

    def build(self):
        url = self.conan_data["sources"][self.version]["url"]
        if (url.endswith("zst")):
            filename = os.path.basename(url)
            download(self, url=url, filename=filename)
            check_output_runner("zstd -d \"%s\"" % filename).strip()
            unzip(self, os.path.splitext(filename)[0]) # Strip .zst extension
        else:
            get(self, **self.conan_data["sources"][self.version])
        if int(self.version) >= 48:
            rename(self, "opt/devkitpro/devkitARM", "devkitARM")

        if int(self.version) >= 51: # TODO: Version r51 have separate repositories for rules and crtls
            git = Git(self, ".")
            git.clone("https://github.com/devkitPro/devkitarm-rules")
            with chdir(self, "devkitarm-rules"):
                #git.checkout("v1.0.0");
                #git.checkout("v1.3.0");
                git.checkout("v1.5.0"); # TODO: Fix version properly. 1.5.0 required for shbin rules

            # Patch hardcoded paths
            replace_in_file(self, "devkitarm-rules/Makefile", "/opt/devkitpro/devkitARM", "$(DEVKITARM)")
            with chdir(self, "devkitarm-rules"):
                autotools = Autotools(self)
                autotools.make()
                autotools.install(args=["DESTDIR="]) # Suppress default DESTDIR argument implicitly added by Conan

            git.clone("https://github.com/devkitPro/devkitarm-crtls")
            # Patch hardcoded paths
            replace_in_file(self, "devkitarm-crtls/Makefile", "/opt/devkitpro/devkitARM", "$(DEVKITARM)")
            with chdir(self, "devkitarm-crtls"):
                autotools = Autotools(self)
                autotools.make()
                autotools.install(args=["DESTDIR="]) # Suppress default DESTDIR argument implicitly added by Conan

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
        self.buildenv_info.define("DEVKITPRO", self.package_folder)
        self.buildenv_info.define("DEVKITARM", toolchain_path)

        # TODO: Add newlib libs and headers

        # TODO: Add binutils path. Arm-non-eabi-as
        #self.env_info.PATH.append(os.path.join(toolchain_path, "bin/gcc/arm-none-eabi/"))
