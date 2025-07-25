#cmake_minimum_required(VERSION 3.15)
#project(PackageTest CXX)
#
#find_package(fcpp CONFIG REQUIRED)
#
#add_executable(example src/example.cpp)
#target_link_libraries(example fcpp::fcpp)

cmake_minimum_required(VERSION 3.28)
project(PackageTest CXX)

find_package(${LIB_NAME} CONFIG REQUIRED)

add_executable(example src/example.cpp)
target_link_libraries(example ${TARGET_NAME})