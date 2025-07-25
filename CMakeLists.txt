cmake_minimum_required(VERSION 3.28)
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/metadata.json" METADATA_JSON)
string(JSON PROJECT_NAME_VALUE ERROR_VARIABLE json_error GET "${METADATA_JSON}" "name")
string(JSON PROJECT_VERSION_VALUE ERROR_VARIABLE json_error GET "${METADATA_JSON}" "version")
string(JSON BUILD_CPPSTD ERROR_VARIABLE json_error GET "${METADATA_JSON}" "build_cppstd")
string(JSON STD_MODULES ERROR_VARIABLE json_error GET "${METADATA_JSON}" "std_modules")
set(LIB_NAME "${PROJECT_NAME_VALUE}")
set(PROJECT_NAMESPACE "${LIB_NAME}")
project(${LIB_NAME} CXX)


# define file search mode (can be adjusted according to the project structure)
set(HEADER_PATTERNS "*.h" "*.hpp")
set(SOURCE_PATTERNS "*.c" "*.cpp")
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
add_library(${LIB_NAME}
        ${SOURCE_FILES}
        ${MODULE_FILES}
)

target_include_directories(${LIB_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(${LIB_NAME} PROPERTIES
        CXX_STANDARD ${BUILD_CPPSTD}
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
        OUTPUT_NAME "${LIB_NAME}"  # export file using lib name
)


# module features are fully activated in C++23 or greater
if(BUILD_CPPSTD VERSION_GREATER_EQUAL 23)

    set_source_files_properties(${MODULE_FILES} PROPERTIES LANGUAGE CXX)

    if(MSVC)
        list(FILTER MODULE_FILES INCLUDE REGEX "\\.ixx$")
    else()
        list(FILTER MODULE_FILES INCLUDE REGEX "\\.cppm$")
    endif()

    if(MSVC)

        # Need improve: if 23, use /std:c++latest, Otherwise unknown to be ignored
        target_compile_options(${LIB_NAME} PRIVATE "/std:c++${BUILD_CPPSTD}")

        set(MODULE_INTERFACE_FILES "")
        foreach(file IN LISTS MODULE_FILES)
            if(file MATCHES "\\.ixx$")
                list(APPEND MODULE_INTERFACE_FILES ${file})
            endif()
        endforeach()
        set_source_files_properties(${MODULE_INTERFACE_FILES} PROPERTIES COMPILE_OPTIONS "/interface")

    elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")

        target_compile_options(${LIB_NAME} PRIVATE
                -fmodules-ts
                $<$<CXX_COMPILER_ID:Clang>:-fimplicit-module-maps>
        )

        if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND STD_MODULES)  # TODO: may be simplified for GCC14+ adaption

            separate_arguments(STD_MODULES_LIST NATIVE_COMMAND "${STD_MODULES}")
            set(GCM_CACHE_DIR "${CMAKE_BINARY_DIR}/gcm.cache")
            file(MAKE_DIRECTORY ${GCM_CACHE_DIR})

            set(STD_GCM_FILES)
            foreach(module IN LISTS STD_MODULES_LIST)
                add_custom_command(
                        OUTPUT "${GCM_CACHE_DIR}/${module}.gcm"
                        COMMAND ${CMAKE_CXX_COMPILER}
                        -fmodules-ts
                        -x c++-system-header
                        ${module}
                        COMMENT "Pre-compiling system module: ${module}"
                        VERBATIM
                )
                list(APPEND STD_GCM_FILES "${GCM_CACHE_DIR}/${module}.gcm")
            endforeach()

            add_custom_target(precompile_std_modules ALL DEPENDS ${STD_GCM_FILES})
            add_dependencies(${LIB_NAME} precompile_std_modules)

            target_compile_options(${LIB_NAME} PRIVATE
                    "-fmodules-cache-path=${GCM_CACHE_DIR}"
            )
        endif()

    endif()

else()
    message(STATUS "C++ standard ${BUILD_CPPSTD} < 23, disabling module support")
endif()


# install targets
install(TARGETS ${LIB_NAME}
        EXPORT ${LIB_NAME}Targets
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
        PUBLIC_HEADER DESTINATION include
        INCLUDES DESTINATION include
)


# install headers
install(DIRECTORY include/
        DESTINATION include
        FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

install(EXPORT ${LIB_NAME}Targets
        FILE ${LIB_NAME}Config.cmake
        NAMESPACE ${PROJECT_NAMESPACE}::
        DESTINATION lib/cmake/${LIB_NAME}
)