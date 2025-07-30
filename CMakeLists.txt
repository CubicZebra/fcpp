cmake_minimum_required(VERSION 3.28)
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/metadata.json" METADATA_JSON)
string(JSON PROJECT_NAME_VALUE ERROR_VARIABLE json_error GET "${METADATA_JSON}" "name")
string(JSON PROJECT_VERSION_VALUE ERROR_VARIABLE json_error GET "${METADATA_JSON}" "version")
string(JSON BUILD_CPPSTD ERROR_VARIABLE json_error GET "${METADATA_JSON}" "build_cppstd")
string(JSON BUILD_CSTD ERROR_VARIABLE json_error GET "${METADATA_JSON}" "build_cstd")
string(JSON STD_MODULES ERROR_VARIABLE json_error GET "${METADATA_JSON}" "std_modules")
set(LIB_NAME "${PROJECT_NAME_VALUE}")
set(PROJECT_NAMESPACE "${LIB_NAME}")
project(${LIB_NAME} LANGUAGES C CXX)


function(parse_conan_deps INPUT_VAR OUTPUT_VAR)

    set(INPUT_STR "${${INPUT_VAR}}")

    string(REPLACE "[" "" CLEANED_STR "${INPUT_STR}")
    string(REPLACE "]" "" CLEANED_STR "${CLEANED_STR}")
    string(REPLACE "'" "" CLEANED_STR "${CLEANED_STR}")

    string(REPLACE ", " ";" LIST_ITEMS "${CLEANED_STR}")

    set(RESULT_LIST "")

    foreach(ITEM IN LISTS LIST_ITEMS)
        list(APPEND RESULT_LIST "${ITEM}")
    endforeach()

    set("${OUTPUT_VAR}" "${RESULT_LIST}" PARENT_SCOPE)
endfunction()


function(split_conan_dependency INPUT_STR PACKAGE_NAME TARGETS)

    if(NOT DEFINED ${INPUT_STR} OR "${${INPUT_STR}}" STREQUAL "")
        message(FATAL_ERROR "Input string is empty or undefined")
    endif()

    string(FIND "${${INPUT_STR}}" "@" AT_POS)
    if(AT_POS EQUAL -1)
        message(FATAL_ERROR "Input string does not contain '@': ${${INPUT_STR}}")
    endif()

    string(SUBSTRING "${${INPUT_STR}}" 0 ${AT_POS} PACKAGE_NAME_RAW)

    math(EXPR AFTER_AT_START "${AT_POS} + 1")
    string(SUBSTRING "${${INPUT_STR}}" ${AFTER_AT_START} -1 TARGETS_RAW)

    set("${PACKAGE_NAME}" "${PACKAGE_NAME_RAW}" PARENT_SCOPE)
    set("${TARGETS}" "${TARGETS_RAW}" PARENT_SCOPE)
endfunction()


# define file search mode (can be adjusted according to the project structure)
set(C_HEADER_PATTERNS "*.h")
set(CPP_HEADER_PATTERNS "*.hpp")
set(C_SOURCE_PATTERNS "*.c")
set(CPP_SOURCE_PATTERNS "*.cpp")
set(MODULE_PATTERNS "*.ixx" "*.cppm")


# auto file collection
file(GLOB_RECURSE C_HEADERS
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${C_HEADER_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

file(GLOB_RECURSE CPP_HEADERS
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${CPP_HEADER_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

file(GLOB_RECURSE C_SOURCES
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${C_SOURCE_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

file(GLOB_RECURSE CPP_SOURCES
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${CPP_SOURCE_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

file(GLOB_RECURSE MODULE_FILES
        LIST_DIRECTORIES false
        CONFIGURE_DEPENDS
        ${MODULE_PATTERNS}
        PATHS "${CMAKE_CURRENT_SOURCE_DIR}/src"
)


# dynamically create lib targets
add_library(${LIB_NAME}_c STATIC ${C_SOURCES})
add_library(${LIB_NAME}_cpp STATIC ${CPP_SOURCES} ${MODULE_FILES})
add_library(${LIB_NAME} INTERFACE)

if(NOT C_DEPS STREQUAL "[]")
    parse_conan_deps(C_DEPS PARSED_C_DEPS)
    foreach (C_ITEM IN LISTS PARSED_C_DEPS)
        split_conan_dependency(C_ITEM C_PKG_NAME C_PKG_TARGETS)
        find_package(${C_PKG_NAME} REQUIRED)
        target_link_libraries(${LIB_NAME}_c PUBLIC ${C_PKG_TARGETS})
    endforeach ()
endif()

if(NOT CPP_DEPS STREQUAL "[]")
    parse_conan_deps(CPP_DEPS PARSED_CPP_DEPS)
    foreach (CPP_ITEM IN LISTS PARSED_CPP_DEPS)
        split_conan_dependency(CPP_ITEM CPP_PKG_NAME CPP_PKG_TARGETS)
        find_package(${CPP_PKG_NAME} REQUIRED)
        target_link_libraries(${LIB_NAME}_cpp PUBLIC ${CPP_PKG_TARGETS})
    endforeach ()
endif()

target_link_libraries(${LIB_NAME} INTERFACE ${LIB_NAME}_c ${LIB_NAME}_cpp)

set_target_properties(${LIB_NAME}_c PROPERTIES
        C_STANDARD ${BUILD_CSTD}
        C_STANDARD_REQUIRED ON
        C_EXTENSIONS OFF
        OUTPUT_NAME "${LIB_NAME}_c"
)

set_target_properties(${LIB_NAME}_cpp PROPERTIES
        CXX_STANDARD ${BUILD_CPPSTD}
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
        OUTPUT_NAME "${LIB_NAME}_cpp"
)

target_include_directories(${LIB_NAME}_c PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_include_directories(${LIB_NAME}_cpp PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
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

        target_compile_options(${LIB_NAME}_cpp PRIVATE
                "$<$<VERSION_GREATER_EQUAL:${BUILD_CPPSTD},23>:/std:c++latest>"
                "$<$<VERSION_LESS:${BUILD_CPPSTD},23>:/std:c++${BUILD_CPPSTD}>"
        )

        set(MODULE_INTERFACE_FILES "")
        foreach(file IN LISTS MODULE_FILES)
            if(file MATCHES "\\.ixx$")
                list(APPEND MODULE_INTERFACE_FILES ${file})
            endif()
        endforeach()
        set_source_files_properties(${MODULE_INTERFACE_FILES} PROPERTIES COMPILE_OPTIONS "/interface")

    elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")

        target_compile_options(${LIB_NAME}_cpp PRIVATE
                -fmodules-ts
                $<$<CXX_COMPILER_ID:Clang>:-fimplicit-module-maps>
        )

        if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND STD_MODULES)

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
            add_dependencies(${LIB_NAME}_cpp precompile_std_modules)

            target_compile_options(${LIB_NAME}_cpp PRIVATE
                    "-fmodules-cache-path=${GCM_CACHE_DIR}"
            )
        endif()

    endif()

else()
    message(STATUS "C++ standard ${BUILD_CPPSTD} < 23, disabling module support")
endif()


if(SHARED_MSG)
    message(STATUS "${SHARED_MSG} use static instead!")
endif()


# install targets
install(TARGETS ${LIB_NAME}_c ${LIB_NAME}_cpp
        EXPORT ${LIB_NAME}Targets
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
)

install(FILES ${C_HEADERS}
        DESTINATION include
        COMPONENT c_headers
)

install(FILES ${CPP_HEADERS}
        DESTINATION include
        COMPONENT cpp_headers
)

install(EXPORT ${LIB_NAME}Targets
        FILE ${LIB_NAME}Config.cmake
        NAMESPACE ${PROJECT_NAMESPACE}::
        DESTINATION lib/cmake/${LIB_NAME}
)
