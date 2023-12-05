cmake_minimum_required(VERSION 3.1.2)
project(picasso)

set(SOURCE_SUBFOLDER ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/source)

add_executable(picasso "${SOURCE_SUBFOLDER}/picasso_assembler.cpp" "${SOURCE_SUBFOLDER}/picasso_frontend.cpp")
target_compile_definitions(picasso PRIVATE "-DPACKAGE_STRING=\"${PACKAGE_STRING}\"")

install(TARGETS picasso RUNTIME DESTINATION bin)
