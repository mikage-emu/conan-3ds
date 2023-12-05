from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command
from conan.api.output import ConanOutput

from conans.util.runners import check_output_runner

import tempfile

import yaml

import os
import shutil

@conan_command(group="Homebrew 3DS development")
def setup_3ds(conan_api: ConanAPI, parser, *args):
    """
    Set up Conan for 3DS homebrew development
    """
    ConanOutput().define_log_level("warning")

    main_profile_path = conan_api.profiles.get_path("devkitarm")

    with tempfile.TemporaryDirectory() as tmpfolder:
        # TODO: Publish repository
        check_output_runner("git clone \"%s\" \"%s\"" % ("TODO_LOCAL_REPOSITORY_HERE", tmpfolder)).strip()

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
