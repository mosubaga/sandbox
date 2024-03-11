cmake_minimum_required(VERSION 3.28)
project(zcurl)

set(CMAKE_CXX_STANDARD 17)

find_package(CURL REQUIRED)
set(CURL_LIBRARY "-lcurl")

add_executable(zcurl main.cpp)

include_directories(${CURL_INCLUDE_DIR})
# target_link_libraries(zcurl ${CURL_LIBRARIES})
target_link_libraries(zcurl CURL::libcurl)


