from conan import ConanFile, tools
from conan.tools.files import chdir, collect_libs, copy, get, patch, replace_in_file, rmdir
from conan.tools.gnu import Autotools, AutotoolsDeps

import glob
import os

class Conan(ConanFile):
    name = '3ds_hbmenu'
    settings = 'compiler', 'build_type'
    description = 'The Homebrew Launcher (hbmenu for short) is the main menu used to list and launch homebrew applications'
    url = 'https://github.com/devkitpro/3ds-hbmenu'

    generators = ['AutotoolsToolchain', 'PkgConfigDeps']

    options = {
        # If true, hbmenu will automatically wait for 3dslink to connect on startup
        'auto_netload': [True, False]
    }
    default_options = {
        'auto_netload': False
    }

    def generate(self):
        tc = AutotoolsDeps(self)
        tc.environment.append("LDFLAGS_CONAN", tc.environment.vars(self)["LDFLAGS"])
        tc.generate()

    def requirements(self):
        self.requires("libctru/[>=2.1.0]")
        self.requires("citro3d/[>=1.7.0]")
        self.requires("tinyxml2/[>=9.0.0]")
        self.requires("libconfig/[>=1.7.3]")
        self.requires("zlib/[>=1.3]")
        pass

    def build_requirements(self):
        self.tool_requires("tex3ds/[>1.0.1]")
        self.tool_requires("dka_3dstools/[>=1.3.1]")
        self.tool_requires("dka_general_tools/[>=1.2.0]")
        self.tool_requires("picasso/[>=2.7.0]")
        pass

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

        # The project Makefiles hardcode CFLAGS and LDFLAGS *and* they expect citro3d to be installed into the libctru library...
        # Patch up the Makefiles so it can pick up our libraries
        with chdir(self, self.source_folder):
            for file in glob.iglob('**/Makefile', recursive=True):
                print("Patching %s" % file)
                replace_in_file(self, file, "CFLAGS	:=", "CFLAGS	:= $(CPPFLAGS)")
                replace_in_file(self, file, "LDFLAGS	=", "LDFLAGS	= $(LDFLAGS_CONAN)")

    def build(self):
        with chdir(self, self.source_folder):
            if self.options.auto_netload:
                replace_in_file(self, os.path.join(self.source_folder, 'source/ui/menu.c'), 'u32 held', 'static int first = 1; if (first) down |= KEY_Y; first = 0;\nu32 held')

            autotools = Autotools(self)
            autotools.make()

    def package(self):
        copy(self, "boot.3dsx", src=self.source_folder, dst=self.package_folder)
