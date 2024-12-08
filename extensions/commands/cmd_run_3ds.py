from conan.api.conan_api import ConanAPI
from conan.api.model import ListPattern
from conan.api.output import ConanOutput
from conan.cli.command import conan_command

try:
    from conan.errors import ConanException
except ImportError:
    from conans.errors import ConanException

from conans.model.package_ref import PkgReference

import argparse
import subprocess
import os

@conan_command(group="Homebrew 3DS development")
def run_3ds(conan_api: ConanAPI, parser, *args):
    """
    Run a host binary from a package
    """
    parser.add_argument('--from', help='Package to run commands from (e.g. ctrtool or ctrtool/1.2.0)')
    parser.add_argument('command', nargs='+', help='Command to run')
    args = vars(parser.parse_args(*args))
    rest = args["command"]
    package_name = args["from"]
    if not package_name:
        package_name = rest[0]

    # Select package ref
    package_ref = package_name
    if not '/' in package_ref:
        package_ref = package_ref + "/*"

    pattern = package_ref + ":*"
    recipes = conan_api.list.select(ListPattern(pattern)).recipes
    if not recipes and not args["from"]:
        raise ConanException("Could not find a package named '%s'. Try using --from" % package_name)
    elif not recipes:
        raise ConanException("Could not find a package named '%s'" % package_name)

    # Results are ordered from oldest to newest, so reverse them for iteration to always pick the newest
    for key, recipe in reversed(recipes.items()):
        for revkey, rev in reversed(recipe["revisions"].items()):
            for package in rev['packages']:
                pref = PkgReference.loads("%s:%s" % (key, package))
                path = conan_api.cache.package_path(pref) + "/bin/"
                if not os.path.exists(path + rest[0]):
                    raise ConanException("Found package folder %s, but it does not contain '%s'" % (path, rest[0]))
                rest[0] = path + rest[0]
                ConanOutput().info("Found binary %s in package %s:%s" % (rest[0], key, package))
                exit(subprocess.run(rest).returncode)

    raise ConanException("%s is not installed. Run \"conan install-3ds --tool %s\" first" % (package_name, package_name))
