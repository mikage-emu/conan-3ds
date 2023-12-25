cmake_minimum_required(VERSION 3.8.2)
project(3dslink)

find_package(ZLIB REQUIRED)

add_executable(3dslink "source_subfolder/host/src/main.c")
target_link_libraries(3dslink PRIVATE ZLIB::ZLIB)
target_compile_definitions(3dslink PRIVATE "-DPACKAGE_STRING=\"${PACKAGE_STRING}\"")

install(TARGETS 3dslink RUNTIME DESTINATION bin)
