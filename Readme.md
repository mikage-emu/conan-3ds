# Conan packages for the 3DS

This is a package repository for everything related to 3DS homebrew development and testing:
Applications, libraries, compilers, and tools. It allows easy set up of a fully functional compiler
toolchain, installation of 3DS libraries, and almost-reproducible builds of packaged 3DS
applications.

The repository is based on the package manager Conan, which allows you to use many of the existing
libraries on [Conan Center](https://conan.io/center). Out of more than 1000 packaged projects, many
will just work for 3DS development. Here are some popular examples:
* The common 3DS base libraries `libctru`, `citro2d`, and `citro3d`
* [fmt](https://fmt.dev) for string formatting
* [Catch2](https://github.com/catchorg/Catch2) for unit testing
* [zlib](https://zlib.net/), [bzip2](https://sourceware.org/bzip2/), [zstd](https://github.com/facebook/zstd), and others for file (de-/)compression
* [Boost](https://www.boost.org/), the C++ library collection

## Features

* Use **hundreds of libraries** available on [Conan Center](https://conan.io/center) for 3DS homebrew development
* Install commonly used **3DS tools** and **applications**: [3dslink](https://github.com/devkitPro/3dslink), [ctrtool](https://github.com/3DSGuy/Project_CTR/tree/master/ctrtool), [hbmenu](https://github.com/devkitPro/3ds-hbmenu)
* **Easy setup**: Three short commands are enough to register the repository, install a toolchain, and build the [3DS examples](https://github.com/devkitPro/3ds-examples)
* **Side-by-side installation** of multiple versions of the same libraries, tools, and even compilers
* **Safe, incremental updates**: You can bump dependency versions in each of your projects individually. If something goes wrong, just go back to the old version!
* **Semi-reproducible builds**: Found an old 3DS homebrew project online but can't build it anymore? No sweat, conan-3ds supports even the most ancient libctru versions from 2015
* Excellent **CMake integration**: Tired of arcane Makefile syntax? Have a look at our [CMake example](examples/3dsapp_textured_cube). Other build systems are still supported of course!
* **Rootless/portable installation**: Working from a public library? You can use conan-3ds without admin privileges

## Installation & quick start

To use the repository, first install the package manager [Conan](https://conan.io/downloads) and
then set up conan-3ds:
```sh
pip install conan
conan config install https://github.com/mikage-emu/conan-3ds
conan setup-3ds
```

To check that everything works, try building the
[3ds-examples](https://github.com/devkitPro/3ds-examples):

```sh
conan install-3ds 3ds_examples --symlink
```

## Usage

### Using packaged tools (3dslink, ctrtool, ...)

To install and run PC tools, use the `install-3ds` and `run-3ds` commands:
```sh
# Install to Conan's package cache (~/.conan2/p)
conan install-3ds --tool 3dslink
# Run the binary
conan run-3ds 3dslink
```

If the tool is part of a package with a different name, you have to use `--package-name`:
```sh
conan run-3ds --package-name dka_3dstools 3dsxdump
```

### Using libraries for homebrew development

To use dependencies in your homebrew app, create a `conanfile.txt` that declares your dependencies
in your project root. The conanfile also needs to specify which build system your app uses in the
`[generators]` section. For reference you can look at the [CMake example project](examples/3dsapp_textured_cube),
which also outlines how to trigger the build itself.

For building apps with `Make`, you'll need to use the `AutotoolDeps` generator instead.
`conan install .` will then generate a `conanbuild.sh` script that sets up your environment for
building.

### Adding new packages

If you want to use a library/tool that is not already packaged here or on [Conan Center](https://conan.io/center),
you need to create a new Conan recipe (`conanfile.py` + `conandata.yml`) for it. For reference you
can look at existing packages:
* [libctru](packages/libctru) for Makefile example (and citro3d for a slightly more complex example)
* [3dslink](packages/3dslink) for an example to wrap a PC tool

When developing new packages, a handy command to test building the package is `conan create . --profile devkitarm62`.

### Full reference

Run `conan --help` to get a full list of commands. You can also use e.g. `conan install-3ds --help`
to learn more about each subcommand specifically.

One feature worth mentioning is support for old versions: If you need to build an ancient version
of `3ds_examples` with an equally old toolchain, you can do so by specifying them explicitly:
```sh
conan list 3ds_examples # list available versions
conan install-3ds 3ds_examples/20170714 --toolchain devkitarm49
```

## Frequently Asked Questions

### Why another package manager for the 3DS?

The package manager `pacman` is already widely used for 3DS homebrew development and is a big leap
forward compared to manual juggling of library dependencies. Sadly it has proven insufficient for
Mikage's requirements. During development, we often encountered several problems:
* Inflexible library versions: Old projects could not be built with newer libctru versions since
  `pacman` only provides the latest version
* Risky updates: Due to lack of side-by-side installation, library updates were an all-or-nothing
  deal that affected all projects simultaneously. This made updates a big, unpredictable,
  irreversible risk, which often led to *days* of unexpected follow-up work
* Manual version tracking: Since no mechanism existed to document version ranges, we had to run our
  own bookkeeping to track which library versions are required by each project
* Many widely used C++ libraries were simply not packaged, making essential things like unit
  testing or logging unnecessarily difficult

These are typical concerns that come up during the development of large, complex software: Mikage
implements various internal debugging tools and a large set of 3DS hardware tests. Furthermore,
we need access to the latest homebrew tools for development but also often required older software
to reproduce specific issues that we didn't see anywhere else. Working within the constraints of
`pacman` was simply not an option.

Unfortunately, the maintainers of the `pacman` setup have shown no interest in addressing these
shortcomings, so we built our own solution that doesn't suffer from any of the listed problems.
If you were happy to use `pacman` so far, it will likely continue to serve you well in the future,
but there's now an option if you need something more sophisticated.

### What's the Catch?

While `conan-3ds` is designed to cover a wide range of use cases, it's a comparatively young
effort. If you are just starting out with programming, adding a novel tool into the mix will make
it difficult to follow existing 3DS homebrew tutorials.

Furthermore, using `conan-3ds` on Windows currently requires the use of WSL, but otherwise should
work fine. Patches are welcome for native integration.

## Credits

Creation of conan-3ds was facilitated by the help and prior work of many people, listed in no
particular order:
* All Conan and Conan Center contributors for creating a versatile package management infrastructure
* devkitPro for their ARM toolchain
* Leseratte for maintaining an archive of devkitARM software
* The various people who tested conan-3ds during early development
