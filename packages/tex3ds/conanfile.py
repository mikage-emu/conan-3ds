from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.files import get

import os

class Conan(ConanFile):
    name = 'tex3ds'
    url = 'https://github.com/devkitPro/tex3ds'
    description = '3DS texture conversion tools'
    _source_subfolder = 'source_subfolder'

    settings = ['os', 'arch', 'compiler', 'build_type']

    exports_sources = ["CMakeLists.txt"]
    generators = ["CMakeToolchain", "CMakeDeps"]

    requires = ["freetype/2.13.2", "imagemagick/7.1.1-22"]

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        os.rename("tex3ds-%s" % self.version, self._source_subfolder)

    def configure(self):
        # Doesn't compile without freetype currently
        #self.options["imagemagick"].freetype = False

        # Somehow these don't link properly with nested dependencies enabled...

        self.options["imagemagick"].with_lcms = False
        self.options["imagemagick"].with_openexr = False
        self.options["imagemagick"].with_openjp2 = False
        self.options["imagemagick"].with_pango = False
        self.options["imagemagick"].with_webp = False
        self.options["imagemagick"].with_xml2 = False

        self.options["freetype"].with_brotli = False
        self.options["freetype"].with_bzip2 = False
        self.options["freetype"].with_png = False
        self.options["freetype"].with_zlib = False

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.install()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending to PATH: " + bindir)
        self.env_info.PATH.append(bindir)
