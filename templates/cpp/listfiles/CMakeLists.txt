cmake_minimum_required(VERSION 3.24)
project(listfiles)

find_package( Boost COMPONENTS filesystem system REQUIRED)
include_directories(... ${Boost_INCLUDE_DIRS})
link_directories(... ${Boost_LIBRARY_DIRS})
message("Found Boost, {${Boost_LIBRARIES}}, at ${Boost_INCLUDE_DIR}")

set(CMAKE_CXX_STANDARD 20)

add_executable(listfiles main.cpp)
target_link_libraries(listfiles Boost::filesystem Boost::system)