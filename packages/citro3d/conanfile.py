from conan import ConanFile, tools
from conan.tools.files import chdir, collect_libs, copy, get, patch, replace_in_file
from conan.tools.gnu import Autotools
from conan.tools.scm import Version

import os

class Conan(ConanFile):
    name = 'citro3d'
    settings = 'compiler', 'build_type'
    description = 'Homebrew PICA200 GPU wrapper library for Nintendo 3DS'
    url = 'https://github.com/fincs/citro3d'

    def requirements(self):
        ver = Version(self.version)
        if ver >= Version('1.7.0'):
            self.requires("libctru/[>=2.1.0]") # 2.1.0 renamed the _3DS define to __3DS__
        elif ver >= Version('1.6.1'):
            self.requires("libctru/[>=2.0.0 <2.1.0]") # 2.0.0 added the gfxScreenSwapBuffers API; 2.1.0 renamed the _3DS define to __3DS__
        elif ver >= Version('1.3.0'):
            # Untested if libctru 1.3.0/1.4.0/1.5.0 work with this, but 1.2.1 doesn't
            self.requires("libctru/[>=1.5.1 <2.0.0]") # 2.0.0 Deprecated gfxConfigScreen (breaking due to -Werror=deprecated-declarations), used up to including citro3d 1.6.0
        else:
            raise Exception("Unrecognized citro3d version")

    exports_sources = ['add_missing_includes.patch', 'add_c3d_unbindprogram.patch']

    generators = "AutotoolsToolchain"

    def source(self):
        strip_root = Version(self.version) >= Version('1.6.0')
        get(self, **self.conan_data["sources"][self.version], strip_root=strip_root)
        patch(self, patch_file=os.path.join(self.export_sources_folder, 'add_c3d_unbindprogram.patch'))

    def build(self):
        with chdir(self, self.source_folder):
            autotools = Autotools(self)
            autotools.make()

    def package(self):
        copy(self, "*", src=self.source_folder, dst=self.package_folder)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
