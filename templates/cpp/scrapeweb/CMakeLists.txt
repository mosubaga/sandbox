cmake_minimum_required(VERSION 3.16)
project(scrapeweb CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(CURL REQUIRED)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GUMBO REQUIRED IMPORTED_TARGET gumbo)

add_executable(scrapeweb main.cpp)

target_link_libraries(scrapeweb PRIVATE CURL::libcurl PkgConfig::GUMBO)
