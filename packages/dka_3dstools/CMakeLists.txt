cmake_minimum_required(VERSION 3.1.2)
project(3dstools)

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/src)

add_executable(3dsxtool "${SOURCE_SUBFOLDER}/3dsxtool.cpp" "${SOURCE_SUBFOLDER}/romfs.cpp")
add_executable(3dsxdump "${SOURCE_SUBFOLDER}/3dsxdump.cpp")
add_executable(smdhtool "${SOURCE_SUBFOLDER}/smdhtool.cpp" "${SOURCE_SUBFOLDER}/lodepng/lodepng.cpp")

install(TARGETS 3dsxtool 3dsxdump smdhtool RUNTIME DESTINATION bin)
