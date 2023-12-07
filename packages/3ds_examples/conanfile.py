from conan import ConanFile, tools
from conan.tools.files import chdir, collect_libs, copy, get, patch, replace_in_file, rmdir
from conan.tools.gnu import Autotools, AutotoolsDeps

import os
import glob

class Conan(ConanFile):
    name = '3ds_examples'
    settings = 'compiler', 'build_type'
    description = 'Examples for 3DS using devkitARM, libctru and citro3d'
    url = 'https://github.com/devkitpro/3ds-examples'

    # TODO: PkgConfigDeps only required starting from 20200716
    generators = ["AutotoolsToolchain", "PkgConfigDeps"]

    # TODO: Make version-specific
    tool_requires = ["dka_general_tools/1.2.0", "dka_pkgconf/2.1.0", "picasso/2.7.0"]

    exports_sources = ['45758185_fix_parallel_building.patch']

    def generate(self):
        tc = AutotoolsDeps(self)
        tc.environment.append("LDFLAGS_CONAN", tc.environment.vars(self)["LDFLAGS"])
        tc.generate()

    def requirements(self):
        if self.version == "20150818-2c57809":
            self.requires("libctru/0.6.0")
        elif int(self.version) > 20230610:
            raise Exception("Unsupported 3ds-examples version")
        elif int(self.version) >= 20220129:
            self.requires("libctru/[>=2.1.0]") # 20220129 requires new link3dsStdio API
            self.requires("citro2d/[>=1.4.0]")
        elif int(self.version) >= 20200716:
            self.requires("libctru/[>=2.0.0]") # 20200716 requires aptSetChainloaderToSelf
            self.requires("citro2d/[>=1.4.0]") # 20200716 requires new text aligment APIs (C2D_AlignRight, ...)
        elif int(self.version) >= 20200417:
            self.requires("libctru/[>=1.6.0 <2.0.0]") # 20200417 requires 1.6.0 for new Mii Selector definitions; 2.0.0 changed aptLaunchLibraryApplet API
            self.requires("citro3d/[<1.6.1]")
            self.requires("citro2d/[>=1.1.0]")
        elif int(self.version) >= 20190102:
            self.requires("citro2d/[>=1.1.0 <1.2.0]") # 20190102 requires 1.1.0 for ellipse rendering functions
        elif int(self.version) >= 20180513:
            self.requires("citro2d/[>=1.0.0 <1.2.0]") # New dependency since 20180513
        elif int(self.version) >= 20170714:
            self.requires("libctru/[<1.6.0]") # 1.6.0 reworked font APIs
            self.requires("citro3d/[<=1.4.0]") # 20170714 requires <= 1.4.0 due to API deprecation
        else:
            raise Exception("Unrecognized 3ds-examples version")

        if int(self.version) >= 20210610:
            # New modplug-decoding example requires libmodplug, which in turn requires zlib
            self.requires("libmodplug/[>=0.8.9.0]")
            self.requires("zlib/[>=1.3]")
            # New box2d example
            self.requires("box2d/[>=2.3.1]")

    def build_requirements(self):
        # TODO: Old versions only
        if self.version == "20150818-2c57809":
            self.tool_requires("aemstro/51bfeef")
        if int(self.version) >= 20220129:
            # Newer smdhtool is needed
            self.tool_requires("dka_3dstools/[>=1.3.1]")
        else:
            # TODO: Move to toolchain?
            self.tool_requires("dka_3dstools/1.1.4")

        if int(self.version) >= 20180513:
            self.tool_requires("tex3ds/[>1.0.1]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

        if self.version == "20190102":
            patch(self, base_path=".", patch_file="45758185_fix_parallel_building.patch")

        if int(self.version) >= 20200716:
            # New opus-decoding example requires opusfile, which is very difficult to get working:
            # - has a dependency on openssl (though the recipe has an option to disable it)
            # - opus fails to build unless we forcefully remove arm_neon.h from devkitARM
            # - the Conan recipe pulls in pthread and dl if the Conan profile uses Linux for its OS
            # As a workaround, we just disable this hence
            rmdir(self, os.path.join(self.source_folder, "audio/opus-decoding/"))

        # The project Makefiles hardcode CFLAGS and LDFLAGS *and* they expect citro3d to be installed into the libctru library...
        # Patch up the Makefiles so it can pick up our libraries
        with chdir(self, self.source_folder):
            for file in glob.iglob('**/Makefile', recursive=True):
                print("Patching %s" % file)
                replace_in_file(self, file, "CFLAGS	:=", "CFLAGS	:= $(CPPFLAGS)", strict=False)
                replace_in_file(self, file, "LDFLAGS	=", "LDFLAGS	= $(LDFLAGS_CONAN)", strict=False)

    def build(self):
        with chdir(self, self.source_folder):
            autotools = Autotools(self)
            # Parallel builds were broken up until Jan 22, 2019
            autotools.make(args=["-j1"])

    def package(self):
        copy(self, "bin/*", src=self.source_folder, dst=self.package_folder)
