// Conan::ImportStart
#include "doctest.hpp"
#include <iostream>
// Conan::ImportEnd



auto version_test_func() {
    std::cout << "the version_test_func function" << std::endl;
};



void stage_a() {}



void stage_b() {}



void stage_c() { stage_b(); }



/**
 * @brief call relation demo
 * @note the call relationship can also be automatically calculated.
 * @ingroup demo
 */
void stage_d() {
    stage_a();
    stage_b();
    stage_c();
}
