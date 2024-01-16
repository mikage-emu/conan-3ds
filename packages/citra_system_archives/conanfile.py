from conan import ConanFile, tools
from conan.tools.files import chdir, copy, get, replace_in_file
from conan.tools.gnu import Autotools

import os

class Conan(ConanFile):
    name = 'citra_system_archives'
    settings = ['os', 'arch', 'compiler', 'build_type']
    description = 'Set of freely distributable system files for use with 3DS emulators'
    url = 'https://github.com/B3n30/citra_system_archives'
    version = '20190812'

    exports_sources = ['info.rsf']

    tool_requires = ['makerom/0.18.4']

    def source(self):
        get(self, 'https://github.com/B3n30/citra_system_archives/archive/f470e0c9d341db73b8a24880295d2eab4cd81660.tar.gz', strip_root=True)

        # Normally, the build scripts build a raw romfs image and convert it to a header file.
        # We want a proper CFA image instead, so we patch the scripts to stop after writing the RomFS contents.
        replace_in_file(self, 'shared_font/run.sh', 'rm -rf romfs', '')
        replace_in_file(self, 'country_list/country-archive.py', 'd = tempfile.mkdtemp()', 'os.mkdir("romfs"); writeToArchive("romfs", archive); return')
        replace_in_file(self, 'mii/mii.py', 'd = tempfile.mkdtemp()', 'os.mkdir("romfs"); Build(inPath, "romfs/CFL_Res.dat"); return')

    def build(self):
        for archive_name in ['bad_word_list', 'country_list', 'mii', 'shared_font']:
            with chdir(self, os.path.join(self.source_folder, archive_name)):
                self.run('./run.sh')
                self.run("makerom -rsf ../info.rsf -o 00000000.app")

    def package(self):
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'bad_word_list'), dst=os.path.join(self.package_folder, '000400db/00010302/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'country_list'), dst=os.path.join(self.package_folder, '0004009b/00010402/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'mii'), dst=os.path.join(self.package_folder, '0004009b/00010202/content'))
        copy(self, "00000000.app", src=os.path.join(self.source_folder, 'shared_font'), dst=os.path.join(self.package_folder, '0004009b/00014002/content'))
