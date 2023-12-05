# CMake 3.8.2 required for cxx_std_11 compile feature
cmake_minimum_required(VERSION 3.8.2)
project(tex3ds)

find_package(ImageMagick COMPONENTS Magick++)
find_package(Freetype)

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/source)

add_executable(tex3ds
    "${SOURCE_SUBFOLDER}/atlas.cpp"
    "${SOURCE_SUBFOLDER}/encode.cpp"
    "${SOURCE_SUBFOLDER}/huff.cpp"
    "${SOURCE_SUBFOLDER}/lzss.cpp"
    "${SOURCE_SUBFOLDER}/magick_compat.cpp"
    "${SOURCE_SUBFOLDER}/rg_etc1.cpp"
    "${SOURCE_SUBFOLDER}/rle.cpp"
    "${SOURCE_SUBFOLDER}/swizzle.cpp"
    "${SOURCE_SUBFOLDER}/tex3ds.cpp")
#target_compile_features(tex3ds PRIVATE cxx_std_11)
target_include_directories(tex3ds PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/include)
target_link_libraries(tex3ds PRIVATE ${CONAN_TARGETS})
target_link_libraries(tex3ds PRIVATE ImageMagick::Magick++)

add_executable(mkbcfnt
    "${SOURCE_SUBFOLDER}/bcfnt.cpp"
    "${SOURCE_SUBFOLDER}/freetype.cpp"
    "${SOURCE_SUBFOLDER}/magick_compat.cpp"
    "${SOURCE_SUBFOLDER}/mkbcfnt.cpp"
    "${SOURCE_SUBFOLDER}/swizzle.cpp"
    "${SOURCE_SUBFOLDER}/threadPool.cpp")
#target_compile_features(mkbcfnt PRIVATE cxx_std_11)
target_include_directories(mkbcfnt PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/include)
target_link_libraries(mkbcfnt PRIVATE ${CONAN_TARGETS})
target_link_libraries(mkbcfnt PRIVATE ImageMagick::Magick++)
target_link_libraries(mkbcfnt PRIVATE Freetype::Freetype)

install(TARGETS tex3ds mkbcfnt RUNTIME DESTINATION bin)
