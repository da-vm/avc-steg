Modified H.264/AVC encoder/decoder that allows for video authentication by embedding MAYO-3 signature in LSB of P-frame motion vectors.

## Dependencies
- [MAYO](https://github.com/PQCMayo/MAYO-C) is required to compile signature algorithms in `process/MAYO`.
- JM (reference H.264 software) requires building of `lencod` and `ldecod` executables in `JM/bin`.
- Signature algorithms `keygen`, `sign`, `verify` require compiling by `gcc -O2 -o <name> <name>.c -I<path>/MAYO-C/include -I<path>/MAYO-C/src/mayo_3 -L<path>/MAYO-C/build/src -DMAYO_VARIANT=MAYO_3 -DMAYO_BUILD_TYPE_AVX2 -lmayo_3 -lmayo_common_sys`.

## Usage
### Key generation and signing
```
python -m exec.signing input_clean.y4m
```
The signing script generates a MAYO-3 keypair and signs the hash of an input video (default: `files/in/input_clean.y4m`). Output signature is stored as `files/in/signature.txt`, keys are stored as `files/MAYO/pk.bin` and `files/MAYO/sk.bin`.

### Embedding
```
python -m exec.embedding signature.txt input_clean.y4m
```
The embedding script converts the signature to a string of bits and calls JM to embed the string into an input video. Output bitstream is stored as `files/temp/output_JMe.h264`.

### Extraction and verification
```
python -m exec.extraction output_JMe.h264
```
The extraction script extracts the motion vectors from the encoded bitstream, recovers the signature and verifies its validity by using the public key. Output `.yuv` video is stored as `files/out/output_JMd.yuv`, and recovered signature is stored as `files/out/recovered_sig.txt`.

## Limitations
- Currently does not natively support playable output video, requires conversion from `.yuv`.
- Assumes knowledge of public key on receiver's end.
- Currently restricted to MAYO-3 signatures.
- Requires input video in `.y4m` format.
