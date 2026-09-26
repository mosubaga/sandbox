cmake_minimum_required(VERSION 3.20)
project(qsr)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Boost REQUIRED COMPONENTS program_options filesystem)

add_executable(qsr main.cpp)
target_link_libraries(qsr PRIVATE Boost::program_options Boost::filesystem)
