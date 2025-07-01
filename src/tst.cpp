// #include <iostream>
// #include "tst.h"
// // #include <Eigen/Dense>
//
//
//
// void tst(){
//
//
//     #ifdef NDEBUG
//     std::cout << "tst/1.0: Hello World Release!\n";
//     #else
//     std::cout << "tst/1.0: Hello World Debug!\n";
//     #endif
//
//     // ARCHITECTURES
//     #ifdef _M_X64
//     std::cout << "  tst/1.0: _M_X64 defined\n";
//     #endif
//
//     #ifdef _M_IX86
//     std::cout << "  tst/1.0: _M_IX86 defined\n";
//     #endif
//
//     #ifdef _M_ARM64
//     std::cout << "  tst/1.0: _M_ARM64 defined\n";
//     #endif
//
//     #if __i386__
//     std::cout << "  tst/1.0: __i386__ defined\n";
//     #endif
//
//     #if __x86_64__
//     std::cout << "  tst/1.0: __x86_64__ defined\n";
//     #endif
//
//     #if __aarch64__
//     std::cout << "  tst/1.0: __aarch64__ defined\n";
//     #endif
//
//     // Libstdc++
//     #if defined _GLIBCXX_USE_CXX11_ABI
//     std::cout << "  tst/1.0: _GLIBCXX_USE_CXX11_ABI "<< _GLIBCXX_USE_CXX11_ABI << "\n";
//     #endif
//
//     // MSVC runtime
//     #if defined(_DEBUG)
//         #if defined(_MT) && defined(_DLL)
//         std::cout << "  tst/1.0: MSVC runtime: MultiThreadedDebugDLL\n";
//         #elif defined(_MT)
//         std::cout << "  tst/1.0: MSVC runtime: MultiThreadedDebug\n";
//         #endif
//     #else
//         #if defined(_MT) && defined(_DLL)
//         std::cout << "  tst/1.0: MSVC runtime: MultiThreadedDLL\n";
//         #elif defined(_MT)
//         std::cout << "  tst/1.0: MSVC runtime: MultiThreaded\n";
//         #endif
//     #endif
//
//     // COMPILER VERSIONS
//     #if _MSC_VER
//     std::cout << "  tst/1.0: _MSC_VER" << _MSC_VER<< "\n";
//     #endif
//
//     #if _MSVC_LANG
//     std::cout << "  tst/1.0: _MSVC_LANG" << _MSVC_LANG<< "\n";
//     #endif
//
//     #if __cplusplus
//     std::cout << "  tst/1.0: __cplusplus" << __cplusplus<< "\n";
//     #endif
//
//     #if __INTEL_COMPILER
//     std::cout << "  tst/1.0: __INTEL_COMPILER" << __INTEL_COMPILER<< "\n";
//     #endif
//
//     #if __GNUC__
//     std::cout << "  tst/1.0: __GNUC__" << __GNUC__<< "\n";
//     #endif
//
//     #if __GNUC_MINOR__
//     std::cout << "  tst/1.0: __GNUC_MINOR__" << __GNUC_MINOR__<< "\n";
//     #endif
//
//     #if __clang_major__
//     std::cout << "  tst/1.0: __clang_major__" << __clang_major__<< "\n";
//     #endif
//
//     #if __clang_minor__
//     std::cout << "  tst/1.0: __clang_minor__" << __clang_minor__<< "\n";
//     #endif
//
//     #if __apple_build_version__
//     std::cout << "  tst/1.0: __apple_build_version__" << __apple_build_version__<< "\n";
//     #endif
//
//     // SUBSYSTEMS
//
//     #if __MSYS__
//     std::cout << "  tst/1.0: __MSYS__" << __MSYS__<< "\n";
//     #endif
//
//     #if __MINGW32__
//     std::cout << "  tst/1.0: __MINGW32__" << __MINGW32__<< "\n";
//     #endif
//
//     #if __MINGW64__
//     std::cout << "  tst/1.0: __MINGW64__" << __MINGW64__<< "\n";
//     #endif
//
//     #if __CYGWIN__
//     std::cout << "  tst/1.0: __CYGWIN__" << __CYGWIN__<< "\n";
//     #endif
// }
//
// void tst_print_vector(const std::vector<std::string> &strings) {
//     for(std::vector<std::string>::const_iterator it = strings.begin(); it != strings.end(); ++it) {
//         std::cout << "tst/1.0 " << *it << std::endl;
//     }
// }


// 1. 全局模块片段：包含传统头文件
module;  // 开始全局模块片段

// 在此包含无法用模块导入的头文件
import <iostream>;  // 标准头文件（不支持模块化），C++23支持模块化导入

// 2. 声明模块实现单元
module tst;  // 实现模块 `tst` 中的函数

// 3. 函数实现（注意：不再需要 `export`）
void tsta() {
    // 原始实现代码保持不变（略）
    #ifdef NDEBUG
        std::cout << "tst/1.0: Hello World Release!\n";
    #else
        std::cout << "tst/1.0: Hello World Debug!\n";
    #endif
        // ...（其他诊断代码）
}

void tst_print_vector(const std::vector<std::string> &strings) {
    for (const auto & string : strings) {
        std::cout << "tst/1.0 " << string << std::endl;
    }
}