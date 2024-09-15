from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import copy, replace_in_file
from conan.tools.scm import Git

import os

class DynarmicConan(ConanFile):
    name = 'dynarmic'
    version = '20240303'
    settings = 'os', 'compiler', 'build_type', 'arch'
    description = 'An ARM dynamic recompiler'
    url = 'https://github.com/ihaveamac/dynarmic'
    license = 'GNU General Public License v2.0'

    #requires = [ 'boost/1.69.0', 'fmt/7.1.3' ]
    requires = [ 'boost/[>=1.57.0]', 'fmt/8.1.1' ]
    generators = "CMakeDeps"

    def source(self):
        git = Git(self)
        git.clone(url='https://github.com/ihaveamac/dynarmic')
        git.folder = "dynarmic"
        git.checkout(commit="a41c380")
        replace_in_file(self, 'dynarmic/CMakeLists.txt', 'find_package(fmt 9', 'find_package(fmt 8')

    def generate(self):
        cmake = CMakeToolchain(self)
        cmake.cache_variables['DYNARMIC_TESTS'] = False
        cmake.cache_variables['DYNARMIC_WARNINGS_AS_ERRORS'] = False
        cmake.cache_variables['DYNARMIC_NO_BUNDLED_FMT'] = True
        # TODO: Disable bundled fmt!
        # TODO: Only compile A32 frontend!
        cmake.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder='dynarmic')
        cmake.build()

    def package(self):
        copy(self, '*', src='dynarmic', dst=self.package_folder)
        copy(self, '*', src='src/dynarmic', dst=os.path.join(self.package_folder, "lib"))
        copy(self, '*', src='externals/mcl/src/', dst=os.path.join(self.package_folder, "lib"))
        copy(self, '*', src='externals/fmt', dst=os.path.join(self.package_folder, "lib"))
        copy(self, '*', src='externals/zydis', dst=os.path.join(self.package_folder, "lib"))

    def package_info(self):
        #self.cpp_info.includedirs = ["source/include"]
        self.cpp_info.includedirs = ["src"]

        # libdynarmic must be listed first for proper link ordering
        self.cpp_info.libdirs = ["externals/zydis", "externals/zydis/zycore", "externals/mcl/src", "externals/fmt"]
        #dep_libs = tools.collect_libs(self)
        #self.cpp_info.libdirs = ["src/dynarmic"]
        #self.cpp_info.libs = tools.collect_libs(self) + dep_libs
        self.cpp_info.libs = ['dynarmic', 'mcl']
        if self.settings.os != "Macos" and self.settings.os != "Android":
            self.cpp_info.libs.append('Zydis');
        self.cpp_info.libdirs = ["externals/zydis", "externals/zydis/zycore", "externals/mcl/src", "externals/fmt", "lib"]
