#include <stdio.h>
#include <stdint.h>
#include "api.h"

int main(int argc, char *argv[]) {
    const char *pk_path = argc > 1 ? argv[1] : "pk_bin";
    const char *sk_path = argc > 2 ? argv[2] : "sk_bin";

    uint8_t pk[CRYPTO_PUBLICKEYBYTES];
    uint8_t sk[CRYPTO_SECRETKEYBYTES];

    if( mayo_keypair_compact(NULL, pk, sk) != MAYO_OK ) {
        fprintf(stderr, "Key Generation failed\n");
        return 1;
    }

    FILE *f = fopen(pk_path, "wb");
    
    if( !f || fwrite(pk, 1, CRYPTO_PUBLICKEYBYTES, f) != CRYPTO_PUBLICKEYBYTES ) {
        fprintf(stderr, "Failed to write public key\n");
        return 1;
    }
    fclose(f);

    f = fopen(sk_path, "wb");

    if( !f || fwrite(sk, 1, CRYPTO_SECRETKEYBYTES, f) != CRYPTO_SECRETKEYBYTES ) {
        fprintf(stderr, "Failed to write secret key\n");
        return 1;
    }
    fclose(f);

    printf("Keys Generated\npk size:  \x1b[32m%d\x1b[m  bytes\n\n", CRYPTO_PUBLICKEYBYTES);
    return 0;
}