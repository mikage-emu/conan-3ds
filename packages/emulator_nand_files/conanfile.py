from conan import ConanFile, tools
from conan.tools.files import chdir, copy, get, rename, replace_in_file, save
from conan.tools.gnu import Autotools

import os

class Conan(ConanFile):
    name = 'emulator_nand_files'
    settings = []
    description = 'Set of freely distributable system files for use with 3DS emulators'
    url = 'https://github.com/mikage-emu/nand-titles'
    version = '20250819'

    tool_requires = ['makerom/0.18.4']

    def source(self):
        get(self, 'https://github.com/mikage-emu/nand-titles/archive/40a138a08420fc13f4444df3321f4a4f8dc7b939.tar.gz', strip_root=True)

    def build(self):
        for archive_name in ['bad_word_list', 'country_list', 'mii', 'nver', 'shared_font']:
            with chdir(self, os.path.join(self.source_folder, archive_name)):
                self.run('./run.sh')

    def package(self):
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'bad_word_list'), dst=os.path.join(self.package_folder, '000400db/00010302/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'country_list'), dst=os.path.join(self.package_folder, '0004009b/00010402/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'mii'), dst=os.path.join(self.package_folder, '0004009b/00010202/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'nver'), dst=os.path.join(self.package_folder, '000400db/00016102/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'shared_font'), dst=os.path.join(self.package_folder, '0004009b/00014002/content'))
        copy(self, "00000000_chn.app", src=os.path.join(self.source_folder, 'shared_font'), dst=os.path.join(self.package_folder, '0004009b/00014102/content'))
        copy(self, "00000000_kor.app", src=os.path.join(self.source_folder, 'shared_font'), dst=os.path.join(self.package_folder, '0004009b/00014202/content'))
        copy(self, "00000000_twn.app", src=os.path.join(self.source_folder, 'shared_font'), dst=os.path.join(self.package_folder, '0004009b/00014302/content'))
