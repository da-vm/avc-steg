#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "api.h"

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <hash.bin> <pk.bin> <signature.txt>\n", argv[0]);
        return 1;
    }

    uint8_t digest[32];
    FILE *f = fopen(argv[1], "rb");
    if (!f || fread(digest, 1, 32, f) != 32) {
        fprintf(stderr, "Failed to read hash\n"); return 1;
    }
    fclose(f);

    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    f = fopen(argv[2], "rb");
    if (!f || fread(pk, 1, CRYPTO_PUBLICKEYBYTES, f) != CRYPTO_PUBLICKEYBYTES) {
        fprintf(stderr, "Failed to read public key\n"); return 1;
    }
    fclose(f);

    uint8_t sig[CRYPTO_BYTES];
    f = fopen(argv[3], "rb");
    if (!f || fread(sig, 1, CRYPTO_BYTES, f) != CRYPTO_BYTES) {
        fprintf(stderr, "Failed to read signature\n"); return 1;
    }
    fclose(f);

    int result = mayo_verify(NULL, digest, 32, sig, pk);

    if (result == MAYO_OK) {
        printf("OK  signature valid\n");
    } else {
        printf("FAIL  signature invalid\n");
    }
    return result;
}