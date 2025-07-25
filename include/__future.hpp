#ifndef __FUTURE_HPP
#define __FUTURE_HPP


#ifndef NUM_CPPSTD
    #define KK 0
    #if defined(_MSVC_LANG)
        #define CPP_STANDARD _MSVC_LANG
    #elif defined(__cplusplus)
        #define CPP_STANDARD __cplusplus
    #else
        #define CPP_STANDARD 201703L  // fallback to C++17
    #endif
#else
    #define KK 1
    #if NUM_CPPSTD == 17
        #define CPP_STANDARD 201703L
    #elif NUM_CPPSTD == 20
        #define CPP_STANDARD 202002L
    #elif NUM_CPPSTD == 23
        #define CPP_STANDARD 202302L
    #else
        #define CPP_STANDARD 201703L  // 无效值回退
    #endif
#endif


// #if defined(_MSVC_LANG)
//     #define CPP_STANDARD _MSVC_LANG
// #elif defined(__cplusplus)
//     #define CPP_STANDARD __cplusplus
// #else
//     #define CPP_STANDARD 201703L  // fallback to C++17
// #endif


#if CPP_STANDARD >= 202302L  // C++23
    #define HAS_CPP23 1
#else
    #define HAS_CPP23 0
#endif

#if CPP_STANDARD >= 202002L  // C++20
    #define HAS_CPP20 1
#else
    #define HAS_CPP20 0
#endif


#endif //__FUTURE_HPP