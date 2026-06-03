from process.process import extract_mvs_from_trace, extract_string_MAYO, extract_bitstring
import sys
import os
import subprocess
import hashlib

BASE   = os.path.expanduser("~/avc-steg")
MAYO   = os.path.join(BASE, "process/MAYO")
JM_BIN = os.path.join(BASE, "JM/bin")
FILES  = os.path.join(BASE, "files")

def run_decoder(h264_file):

    h264_path = os.path.join(FILES, "temp", h264_file)
    cfg_path  = os.path.join(FILES, "temp", "tmp_decoder.cfg")
    mv_path   = os.path.join(FILES, "temp", "JMd_mv.txt")

    with open(cfg_path, "w") as f:
        f.write(f"InputFile = {h264_path}\n")
        f.write(f"OutputFile = {FILES}/out/output_JMd.yuv")
    
    subprocess.run(f"cd {JM_BIN} && ./ldecod.exe -f {cfg_path} > {mv_path} 2>&1", shell=True, check=True)

    return mv_path

def verify(input_file, signature_path):
    input_path  = os.path.join(FILES, "in", input_file)
    hash_path   = os.path.join(FILES, "MAYO", "recovered_hash.bin")
    pk_path     = os.path.join(FILES, "MAYO", "pk.bin")

    with open(input_path, "rb") as f:
        digest = hashlib.sha256(f.read()).digest()
    with open(hash_path, "wb") as f:
        f.write(digest)

    subprocess.run([os.path.join(MAYO, "verify"), hash_path, pk_path, signature_path], check=True)

if __name__ == "__main__":
    h264_file = sys.argv[1]
    
    mv_txt = run_decoder(h264_file)
    mv_array = extract_mvs_from_trace(mv_txt)
    signature = extract_string_MAYO(mv_array)
    signature_path = os.path.join(FILES, "out", "recovered_sig.txt")
    with open(signature_path, "wb") as f:
        f.write(signature)
    print(f"Recovered \x1b[32m{len(signature)}\x1b[m bytes -> {signature_path}")
    verify("input_clean.y4m", signature_path)
