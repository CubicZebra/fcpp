#pragma once
#include <vector>
#include <string>


/**
 * @defgroup tst
 * @mainpage
 * have to add some text for main page
 */


/**
 * @brief Outputs diagnostic information about the build environment and configuration.
 *
 * This function prints various details about the current build environment to the standard output.
 * The information includes the build type (Debug or Release), target architecture macros,
 * compiler versions, MSVC runtime configurations, and active subsystems.
 * It is primarily intended for debugging and verifying the build setup.
 *
 * The output is conditional based on preprocessor directives, ensuring that only relevant
 * information for the current build environment is displayed.
 * @exporter
 */
void tsta();

/**
 * @brief this is a test function
 * @exporter
 * @details some detailed text here
 */
void tst_print_vector(const std::vector<std::string> &strings);