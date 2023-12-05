cmake_minimum_required(VERSION 3.1.2)
project(3dstools)

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder)

add_executable(bin2s "${SOURCE_SUBFOLDER}/bin2s.c")
target_compile_definitions(bin2s PRIVATE PACKAGE_STRING="bin2s")
add_executable(padbin "${SOURCE_SUBFOLDER}/padbin.c")
add_executable(raw2c "${SOURCE_SUBFOLDER}/raw2c.c")
add_executable(bmp2bin "${SOURCE_SUBFOLDER}/bmp2bin.cpp")

install(TARGETS bin2s padbin raw2c bmp2bin RUNTIME DESTINATION bin)
