cmake_minimum_required(VERSION 3.24)
project(textured_cube)

find_program(CTR_SMDHTOOL_EXE NAMES smdhtool)
find_program(CTR_3DSXTOOL_EXE NAMES 3dsxtool)
find_program(CTR_PICASSO_EXE NAMES picasso)
find_program(CTR_TEX3DS_EXE NAMES tex3ds)
find_program(DKP_BIN2S NAMES bin2s)

find_package(libctru REQUIRED)
find_package(citro3d REQUIRED)

find_file(CTR_DEFAULT_ICON NAMES default_icon.png HINTS "${libctru_RES_DIRS_RELEASE}")

ctr_add_graphics_target(kitten_data IMAGE OPTIONS -f auto-etc1 -z auto INPUTS gfx/kitten.png)
dkp_add_embedded_binary_library(kitten kitten_data)

ctr_add_shader_library(shader_data source/vshader.v.pica)
dkp_add_embedded_binary_library(shader shader_data)

add_executable(textured_cube source/main.c)
target_link_libraries(textured_cube PRIVATE libctru::libctru citro3d::citro3d kitten shader)

ctr_create_3dsx(textured_cube NO_SMDH)
