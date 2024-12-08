from conan.api.conan_api import ConanAPI
from conan.cli.command import conan_command
from conan.api.output import ConanOutput

try:
    from conan.errors import ConanException
except ImportError:
    from conans.errors import ConanException

import argparse
import subprocess

def try_parse_number(str: str):
    try:
        return int(str)
    except ValueError:
        return None;

@conan_command(group="Homebrew 3DS development")
def install_3ds(conan_api: ConanAPI, parser, *args):
    """
    Install a 3DS homebrew library/application package
    """
    parser.add_argument('package-name', help='Package to install (e.g. libctru or libctru/2.3.0)')
    parser.add_argument('-t', '--toolchain', metavar="<N>", help='devkitARM version to compile with', default="latest")
    parser.add_argument('--tool', action='store_true', help='Install tools to run the build machine')
    args = vars(parser.parse_args(*args))

    # Select toolchain
    toolchain = try_parse_number(args["toolchain"])
    if args["tool"]:
        toolchain = "default"
    elif toolchain != None:
        toolchain = "devkitarm%s" % toolchain
    elif args["toolchain"] == "latest":
        toolchain = conan_api.profiles.list()[-1]
        ConanOutput().status("Auto-selecting toolchain %s" % toolchain)
    elif toolchain == None:
        conan_api.profiles.get_profile([args["toolchain"]]) # Check if the profile exists
        toolchain = args["toolchain"]

    # Select package ref
    package_ref = args["package-name"]
    if not '/' in package_ref:
        package_ref = package_ref + "/*"

    recipes = conan_api.search.recipes(package_ref)
    if len(recipes) == 0:
        raise ConanException("No packages named %s found" % args["package-name"])
    package_ref = recipes[0]

    ConanOutput().status("Candidates: %s" % recipes)
    ConanOutput().highlight("Selecting latest: %s" % package_ref)

    # Initiate install
    command = "conan install --%srequires %s -pr %s --build=missing" % (("tool-" if args["tool"] else ""), package_ref, toolchain)
    ConanOutput().status("\nRunning: %s" % command)
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    if process.returncode:
        ConanOutput().write("\n")
        ConanOutput().error("Install of %s failed" % package_ref);
        return

    # TODO: Double check this is prints the correct folder
    rev = next(iter(conan_api.list.packages_configurations(conan_api.list.latest_recipe_revision(package_ref))))
    print("Success: Installed %s to %s" % (package_ref, conan_api.cache.package_path(rev)))
