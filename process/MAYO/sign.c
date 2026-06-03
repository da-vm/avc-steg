#include <stdio.h>
#include <stdint.h>
#include "api.h"

int main( int argc, char *argv[] ) {
    uint8_t digest[32];

    FILE *f = fopen(argv[1], "rb");
    if( !f || fread(digest, 1, 32, f) != 32 ) {
        fprintf(stderr, "Failed to read hash\n");
        return 1;
    }
    fclose(f);

    uint8_t sk[CRYPTO_SECRETKEYBYTES];
    f = fopen(argv[2], "rb");
    if (!f || fread(sk, 1, CRYPTO_SECRETKEYBYTES, f) != CRYPTO_SECRETKEYBYTES) {
        fprintf(stderr, "Failed to read secret key\n"); return 1;
    }
    fclose(f);

    uint8_t sm[CRYPTO_BYTES + 32];
    size_t smlen;
    if (mayo_sign(NULL, sm, &smlen, digest, 32, sk) != MAYO_OK) {
        fprintf(stderr, "Signing failed\n"); return 1;
    }

    f = fopen(argv[3], "wb");
    if (!f || fwrite(sm, 1, CRYPTO_BYTES, f) != CRYPTO_BYTES) {
        fprintf(stderr, "Failed to write signature\n"); return 1;
    }
    fclose(f);

    printf("Signature written\nsig size: \x1b[32m%d\x1b[m bytes -> %s\n", CRYPTO_BYTES, argv[3]);
    return 0;
}
