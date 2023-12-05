cmake_minimum_required(VERSION 3.8.2)
project(citro2d)

find_package(citro3d)

enable_language(C ASM)

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/source)

add_library(citro2d
    "${SOURCE_SUBFOLDER}/base.c"
#    "${SOURCE_SUBFOLDER}/font.c" # TODO: Only 1.2.0 and upwards
    "${SOURCE_SUBFOLDER}/spritesheet.c"
    "${SOURCE_SUBFOLDER}/text.c")
target_include_directories(citro2d PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/include)
#target_link_libraries(citro2d PRIVATE ${CONAN_TARGETS})
target_link_libraries(citro2d PRIVATE citro3d::citro3d)

add_custom_command(
    OUTPUT render2d.shbin
    COMMAND picasso -o render2d.shbin "${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/source/render2d.v.pica"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})
add_custom_command(
    OUTPUT render2d_shbin.h render2d_shbin.s
    COMMAND bin2s -H render2d_shbin.h render2d.shbin > render2d_shbin.s
    DEPENDS render2d.shbin
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(citro2d PUBLIC shaders_bin)
target_sources(citro2d PRIVATE render2d_shbin.s)
target_include_directories(citro2d PRIVATE ${CMAKE_CURRENT_LIST_DIR})

# TODO: Add library and include targets
install(TARGETS citro2d RUNTIME DESTINATION bin)
