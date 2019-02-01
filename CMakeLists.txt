cmake_minimum_required(VERSION 3.13)
project(fifteen-puzzle-solver)

set(CMAKE_CXX_STANDARD 17)
SET(CMAKE_CXX_COMPILER /usr/bin/clang++)

set(CXX_FLAGS "-Wall -pedantic -O3 -g")

set(SOURCES "")
set(HEADERS "")

include_directories(${CMAKE_SOURCE_DIR}/src)

add_subdirectory(src)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX_FLAGS}")

add_executable(fifteen_puzzle_solver ${SOURCES} ${HEADERS})