cmake_minimum_required(VERSION 3.21)
project(untitled)

set(CMAKE_CXX_STANDARD 14)

include_directories(../LabyrinthExplorer)

add_executable(untitled main.cpp ../LabyrinthExplorer/explorer.h ../LabyrinthExplorer/explorer.cpp ../LabyrinthExplorer/coor.cpp ../LabyrinthExplorer/labirinto.cpp)

