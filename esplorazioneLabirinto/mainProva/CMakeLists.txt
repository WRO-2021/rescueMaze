cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

include_directories(..)

add_executable(untitled main.cpp ../explorer.h ../explorer.cpp ../coor.cpp ../labirinto.cpp)

