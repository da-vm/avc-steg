import sys
import os
import subprocess
import hashlib

BASE   = os.path.expanduser("~/avc-steg")
MAYO   = os.path.join(BASE, "process/MAYO")
FILES  = os.path.join(BASE, "files")

def keygen():
    pk_path = os.path.join(FILES, "MAYO", "pk.bin")
    sk_path = os.path.join(FILES, "MAYO", "sk.bin")

    subprocess.run([os.path.join(MAYO, "keygen"), pk_path, sk_path], check=True)

def sign(input_file):
    input_path  = os.path.join(FILES, "in", input_file)
    hash_path   = os.path.join(FILES, "MAYO", "hash.bin")
    sk_path     = os.path.join(FILES, "MAYO", "sk.bin")
    sig_path    = os.path.join(FILES, "in", "signature.txt")

    with open(input_path, "rb") as f:
        digest = hashlib.sha256(f.read()).digest()
    with open(hash_path, "wb") as f:
        f.write(digest)

    subprocess.run([os.path.join(MAYO, "sign"), hash_path, sk_path, sig_path], check=True)

if __name__ == "__main__":
    input_file = sys.argv[1]
    keygen()
    sign(input_file)