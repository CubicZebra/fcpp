cmake_minimum_required(VERSION 3.28)
project(PackageTest C CXX)


find_package(${LIB_NAME} CONFIG REQUIRED)
add_executable(example src/example.cpp)
target_link_libraries(example PRIVATE ${DEP_TARGETS})
target_include_directories(example PRIVATE ${${LIB_NAME}_INCLUDE_DIRS})