cmake_minimum_required(VERSION 3.28)
set(PROJECT_NAME "fcpp")
set(PROJECT_NAMESPACE "${PROJECT_NAME}")
project(${PROJECT_NAME} CXX)


# define file search mode (can be adjusted according to the project structure)
set(HEADER_PATTERNS "*.h" "*.hpp" "*.hxx")
set(SOURCE_PATTERNS "*.c" "*.cpp" "*.cxx")
set(MODULE_PATTERNS "*.ixx" "*.cppm")


# auto file collection
file(GLOB_RECURSE PUBLIC_HEADERS
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${HEADER_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

file(GLOB_RECURSE SOURCE_FILES
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${SOURCE_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

file(GLOB_RECURSE MODULE_FILES
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${MODULE_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/src"
)


# create lib targets
add_library(${PROJECT_NAME}
        ${SOURCE_FILES}
        ${MODULE_FILES}
)

target_include_directories(${PROJECT_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(${PROJECT_NAME} PROPERTIES
        CXX_STANDARD 23
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
        OUTPUT_NAME "${PROJECT_NAME}"  # export file using project name
)


# diverse on platforms
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE "/std:c++latest")
    set_source_files_properties(${MODULE_FILES} PROPERTIES COMPILE_OPTIONS "/interface")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(${PROJECT_NAME} PRIVATE -fmodules-ts)
    set_source_files_properties(${MODULE_FILES} PROPERTIES COMPILE_FLAGS "-fmodules-ts")
else()
    message(WARNING "Unsupported compiler for C++ modules: ${CMAKE_CXX_COMPILER_ID}")
endif()
set_source_files_properties(${MODULE_FILES} PROPERTIES LANGUAGE CXX)


# install targets
install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}Targets
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
        PUBLIC_HEADER DESTINATION include
        INCLUDES DESTINATION include
)


# install headers
install(DIRECTORY include/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp" PATTERN "*.hxx"
)

install(EXPORT ${PROJECT_NAME}Targets
        FILE ${PROJECT_NAME}Config.cmake
        NAMESPACE ${PROJECT_NAMESPACE}::
        DESTINATION lib/cmake/${PROJECT_NAME}
)
