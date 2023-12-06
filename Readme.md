# Conan packages for the 3DS

This is a package repository for everything related to 3DS homebrew development and testing:
Applications, libraries, and tools. It allows easy set up of a fully functional compiler toolchain,
installation of 3DS libraries, and almost-reproducible builds of packaged 3DS applications.

The repository is based on the package manager Conan, which allows you to use many of the existing
libraries on [Conan Center](https://conan.io/center).

## Why another package manager for the 3DS?

To be written later.

## Installation

To use the repository, first install the package manager [Conan](https://conan.io/downloads) and
then set up conan-3ds:
```sh
$ pip install conan
$ conan config install https://github.com/mikage-emu/conan-3ds
$ conan setup-3ds
```

This is safe to run for existing Conan setups as well, since it won't overwrite any previous
configuration other than conan-3ds's own.

## Usage

Proper usage instructions will be provided in the future. For now, try building the
[3ds-examples](https://github.com/devkitPro/3ds-examples):
```sh
$ conan install-3ds 3ds-examples
```

This will install the latest available package version. You can also install old versions if
needed, though you may be prompted to specify an old toolchain to use:
```sh
$ conan install-3ds 3ds_examples/20170714 --toolchain devkitarm49
```
