#ifndef __FUTURE_H
#define __FUTURE_H

#ifdef __cplusplus
extern "C" {
#endif

#if defined(__STDC_VERSION__)
    #define C_STANDARD __STDC_VERSION__
#elif defined(__STDC__)
    #define C_STANDARD 199409L
#else
    #define C_STANDARD 201112L
#endif

#if C_STANDARD >= 202311L  // C23
    #define HAS_C23 1
#endif
#if C_STANDARD >= 201710L  // C17
    #define HAS_C17 1
#endif
#if C_STANDARD >= 201112L  // C11
    #define HAS_C11 1
#endif

#if !defined(HAS_C11)
    #error "Requires at least C11 standard. Please enable C11 or later in your compiler settings."
#endif

#if defined(__GNUC__)
    #define GCC_EXTENSION 1
#endif
#if defined(_MSC_VER)
    #define MSVC_EXTENSION 1
#endif

#ifdef __cplusplus
}
#endif

#endif //__FUTURE_H
