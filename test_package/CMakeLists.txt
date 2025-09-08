cmake_minimum_required(VERSION 3.28)
project(PackageTest C CXX)


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


add_executable(main main.cpp)


if(NOT CXX_DEPS STREQUAL "[]")
    parse_conan_deps(CXX_DEPS PARSED_CXX_DEPS)
    foreach (CXX_ITEM IN LISTS PARSED_CXX_DEPS)
        split_conan_dependency(CXX_ITEM CXX_PKG_NAME CXX_PKG_TARGETS)
        find_package(${CXX_PKG_NAME} REQUIRED)
        target_link_libraries(main PRIVATE ${CXX_PKG_TARGETS})
    endforeach ()
endif()

target_include_directories(main PRIVATE ${${LIB_NAME}_INCLUDE_DIRS})


if (TRIGGER_TESTS)
    find_package(${LIB_NAME} REQUIRED)
    find_package(GTest REQUIRED)
    enable_testing()

    file(GLOB TEST_SOURCES_U "test/unit/*.cpp")
    add_executable(unit_tests ${TEST_SOURCES_U})
    target_link_libraries(unit_tests PRIVATE ${LIB_NAME}::${LIB_NAME} GTest::gtest)
    add_test(NAME unit_tests COMMAND unit_tests)

    file(GLOB TEST_SOURCES_S "test/stress/*.cpp")
    add_executable(stress_tests ${TEST_SOURCES_S})
    target_link_libraries(stress_tests PRIVATE ${LIB_NAME}::${LIB_NAME} GTest::gtest)
    add_test(NAME stress_tests COMMAND stress_tests)
endif ()
