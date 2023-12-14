## 3DS homebrew using conan-3ds and CMake

Simple CMake-based homebrew application adapted from [3ds-examples](https://github.com/devkitPro/3ds-examples).

```sh
mkdir build
cd build
conan install ../conanfile.txt -of . -pr devkitarm53 --build=missing
cmake -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
```
