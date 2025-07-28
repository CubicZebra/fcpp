//! Conan::ImportStart
#include <ctest.h>
#include <stdio.h>
#include <zlib.h>
#define PCRE2_CODE_UNIT_WIDTH 8
#include <pcre2.h>
//! Conan::ImportEnd


/**
 * @brief the C function
 * @exporter
 */
void test_c_compiler() {
    _Static_assert(1, "for C Compiler only");  // _Static_assert: C only syntax
    printf("C Compiler is ready!\n");
}


/**
 * @brief zlib requirement test in C compiler
 * @exporter
 */
void test_c_zlib() {
    char in[] = "Hello, zlib in C!";
    Byte out[128], rec[128];
    uLong len_out = 128, len_rec = 128;
    compress(out, &len_out, in, strlen(in)+1);
    uncompress(rec, &len_rec, out, len_out);
    printf("Original: %s; Decompressed: %s; zlib in C test done!\n", in, rec);
}


/**
 * @brief pcre2 requirement test in C compiler
 * @exporter
 */
void test_c_pcre() {
    pcre2_code *re = pcre2_compile((PCRE2_SPTR)"a", PCRE2_ZERO_TERMINATED, 0, NULL, NULL, NULL);
    int rc = pcre2_match(re, (PCRE2_SPTR)"abc", 3, 0, 0, NULL, NULL);
    printf(rc >= 0 ? "PCRE2 test: Match\n" : "PCRE2 test: No match\n");
    pcre2_code_free(re);
}