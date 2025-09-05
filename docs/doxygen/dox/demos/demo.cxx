// demo.cxx
#include "MyLibrary.h"
#include <iostream>

int main() {
    if (!MyLibrary::init()) {
        std::cerr << "init failure!" << std::endl;
        return -1;
    }

    MyLibrary::process("hello");

    MyLibrary::cleanup();
    return 0;
}