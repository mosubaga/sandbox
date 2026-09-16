#!/bin/bash

BOOST_PREFIX=$(brew --prefix boost)
g++ -O2 -std=c++17 main.cpp -o qprep \
    -I"${BOOST_PREFIX}/include" \
    -L"${BOOST_PREFIX}/lib" \
    -lboost_filesystem -lboost_regex -lboost_program_options -lboost_iostreams