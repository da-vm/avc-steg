import re
import os
import numpy as np

BASE  = os.path.expanduser("~/avc-steg")
FILES = os.path.join(BASE, "files")

def process_txt(txt_file):
    '''
    Takes a .txt file and converts its contents to str
    '''
    txt_path = os.path.join(FILES, "in", txt_file)
    
    with open(txt_path, 'rb') as f:
        data = f.read()
    
    return data

def process_string(msg):
    '''
    Takes a string and converts it to 8-bit binary.
    Prepends the length of the input string and returns the output string of bits.
    '''

    if len(msg) > 2**8:
        raise Exception("Input message too long; length must be at most 256 characters.")
        
    pad_bits = format(len(msg), '08b')

    msg_bits = ''.join(format(ord(c),'08b') for c in msg)

    total_bits = pad_bits + msg_bits

    return total_bits

def process_sig(msg):

    return ''.join(format(b,'08b') for b in msg)

def extract_mvs_from_trace(mv_txt):

    mv_list = []

    with open(mv_txt, 'r') as file:

        for line in file:

            match = re.match(r'^(\d+)  (-?\d+)$', line)

            if match:

                frame = int(match.group(1))
                mv_x = int(match.group(2))
                mv_list.append((frame, mv_x))

    return np.array(mv_list, dtype=int)

def extract_bitstring(array, nbits):

    bits = []

    index_array = np.where(~((array[:,1] > -3) & (array[:,1] < 2)))[0]

    i = 0

    while len(bits) < nbits and i < len(index_array):
        bits.append(str(array[index_array[i],1] & 1))
        i += 1

    return ''.join(bits)

def extract_string(array):

    pad_bits = extract_bitstring(array, 8)
    string_length = int(pad_bits, 2)

    total_length = 8 + string_length * 8
    total_bits = extract_bitstring(array, total_length)

    msg_bits = total_bits[8:]

    msg_chars = [chr(int(msg_bits[i:i+8], 2)) for i in range(0, len(msg_bits), 8)]

    return ''.join(msg_chars)

def extract_string_MAYO(array):

    sig_bitlength = 681 * 8

    sig_bits = extract_bitstring(array, sig_bitlength)

    sig_bytes = bytes([int(sig_bits[i:i+8], 2) for i in range(0, len(sig_bits), 8)])

    return sig_bytes

def extract_string_HAWK(array):

    sig_bitlength = 1221 * 8

    sig_bits = extract_bitstring(array, sig_bitlength)

    sig_bytes = bytes([int(sig_bits[i:i+8], 2) for i in range(0, len(sig_bits), 8)])

    return sig_bytes

def extract_string_SQIsign(array):

    sig_bitlength = 148 * 8

    sig_bits = extract_bitstring(array, sig_bitlength)

    sig_bytes = bytes([int(sig_bits[i:i+8], 2) for i in range(0, len(sig_bits), 8)])

    return sig_bytes