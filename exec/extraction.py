from process.process import extract_mvs_from_trace, extract_string, extract_bitstring
import sys
import os
import subprocess

BASE   = os.path.expanduser("~/avc-steg")
JM_BIN = os.path.join(BASE, "JM/bin")
FILES  = os.path.join(BASE, "files")

def run_decoder(h264_file):

    h264_path = os.path.join(FILES, h264_file)
    cfg_path  = os.path.join(FILES, "tmp_decoder.cfg")
    mv_path   = os.path.join(FILES, "JMd_mv.txt")

    with open(cfg_path, "w") as f:
        f.write(f"InputFile = {h264_path}\n")
        f.write(f"OutputFile = {FILES}/output_JMd.yuv")
    
    subprocess.run(f"cd {JM_BIN} && ./ldecod.exe -f {cfg_path} > {mv_path} 2>&1", shell=True, check=True)

    return mv_path

if __name__ == "__main__":
    h264_file = sys.argv[1]
    
    mv_txt = run_decoder(h264_file)
    mv_array = extract_mvs_from_trace(mv_txt)
    text = extract_string(mv_array)
    print(f"Recovered message: {text}")