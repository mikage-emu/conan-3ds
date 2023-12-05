from conan import ConanFile
from conan.tools.files import copy
from conan.tools.scm import Git

import os

class Conan(ConanFile):
    name = 'aemstro'
    settings = None
    description = "Set of tools used to disassemble and assemble shader code for DMP's MAESTRO shader extension used in the 3DS's PICA200 GPU"
    url = 'https://github.com/smealum/aemstro'
    version = "51bfeef"

    _source_subfolder = 'libctru'

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/smealum/aemstro")
        git.folder = "aemstro"
        git.checkout(commit=self.version)

    def package(self):
        copy(self, "*", src="aemstro", dst=self.package_folder)

    def package_info(self):
        self.cpp_info.bindirs = [self.package_folder]
        self.buildenv_info.define("AEMSTRO", os.path.join(self.package_folder))
