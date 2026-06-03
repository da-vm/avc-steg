from process.process import process_txt, process_sig
import sys
import os
import subprocess

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

BASE   = os.path.expanduser("~/avc-steg")
JM_BIN = os.path.join(BASE, "JM/bin")
FILES  = os.path.join(BASE, "files")

def run_encoder(secret_bits, input_file, output_file):
    # secret_path = os.path.join(FILES, secret_file)
    input_path  = os.path.join(FILES, "in", input_file)
    output_path = os.path.join(FILES, "temp", output_file)
    cfg_path = os.path.join(FILES, "temp", "tmp_encoder.cfg")

    with open(cfg_path, "w") as f:
        f.write(f"InputFile = {input_path}\n")
        f.write(f"OutputFile = {output_path}\n")
        f.write(f"SecretBits = {secret_bits}\n")

    subprocess.run(f"cd {JM_BIN} && ./lencod.exe -f {cfg_path} > /dev/null 2>&1", shell=True, check=True)

if __name__ == "__main__":
    secret_file = sys.argv[1]
    input_file  = sys.argv[2]
    secret_string = process_txt(secret_file)
    secret_bits = process_sig(secret_string)
    run_encoder(secret_bits, input_file, "output_JMe.h264")