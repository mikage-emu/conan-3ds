from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import copy, replace_in_file
from conan.tools.scm import Git

import os

class CtrConan(ConanFile):
    name = 'nihstro'
    version = '0.1-e924e21'
    url = 'https://github.com/neobrain/nihstro'
    description = '3DS shader assembler and disassembler'

    settings = ['os', 'arch', 'compiler', 'build_type']

    generators = ["CMakeToolchain", "CMakeDeps"]

    # TODO: Add option for header-only build

    #requires = 'boost/1.83.0'

    def source(self):
        git = Git(self)
        git.clone(url='https://github.com/neobrain/nihstro', target='.')
        git.checkout('e924e21')

    #def build(self):
    #    cmake = CMake(self)
    #    cmake.configure()
    #    cmake.build()

    def package(self):
        #cmake = CMake(self)
        #cmake.configure()
        #cmake.install()

        copy(self, "*.h", "include/nihstro", os.path.join(self.package_folder, "include", "nihstro"))
