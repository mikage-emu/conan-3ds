from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command
from conan.api.output import ConanOutput

from conans.util.runners import check_output_runner
try:
    from conan.errors import ConanException
except ImportError:
    from conans.errors import ConanException

import tempfile

import yaml

import os
import shutil

@conan_command(group="Homebrew 3DS development")
def setup_3ds(conan_api: ConanAPI, parser, *args):
    """
    Set up Conan for 3DS homebrew development
    """
    args = parser.parse_args(*args)

    main_profile_path = conan_api.profiles.get_path("devkitarm")

    try:
        conan_api.profiles.get_default_build()
    except ConanException:
        print("No compiler set up for Conan, auto-detecting:")
        default_profile = conan_api.profiles.detect()
        print(default_profile)
        # TODO: Double-check that the compiler is set. Otherwise, point user to download Visual Studio 2022 Build Tools
        file = open(os.path.join(os.path.dirname(main_profile_path), "default"), 'x')
        file.write(str(default_profile))
        file.close()

    ConanOutput().define_log_level("warning")

    with tempfile.TemporaryDirectory() as tmpfolder:
        check_output_runner("git clone \"%s\" \"%s\"" % ("https://github.com/mikage-emu/conan-3ds.git", tmpfolder)).strip()

        # Export package recipes
        packages_folder = os.path.join(tmpfolder, "packages")
        for recipe in os.listdir(packages_folder):
            conanfile = os.path.join(packages_folder, recipe, "conanfile.py")
            conandata_path = os.path.join(packages_folder, recipe, "conandata.yml")
            if not os.path.exists(conandata_path):
                print("Installing package recipe %s" % recipe)
                conan_api.export.export(conanfile, None, None, None, None)
            else:
                with open(conandata_path, 'r') as file:
                    conandata = yaml.safe_load(file)

                for version in conandata["sources"]:
                    print("Installing package recipe %s/%s" % (recipe, version))
                    conan_api.export.export(conanfile, None, version, None, None)
                    if recipe == "devkitarm":
                        # Create a fixed-version profile for this toolchain
                        profile_path = main_profile_path + version
                        print("  Registering toolchain profile %s" % profile_path)
                        shutil.copyfile(main_profile_path, profile_path)
