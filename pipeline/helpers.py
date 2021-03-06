import os
import shutil

from .constants import *

def find_mean(sum, divisor):
    if divisor == 0:
        return 0
    return float(sum)/divisor

def timestamp():
    import datetime
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def print_error(err_msg):
    print(err_msg)
    with open(err_file, 'a') as fout:
        fout.write(f"{timestamp()} {err_msg}\n")

def print_log(log_msg):
    print(log_msg)
    with open(log_file, 'a') as fout:
        fout.write(f"{timestamp()} {log_msg}\n")

def create_dir_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def delete_dir_if_exist(path):
  if os.path.exists(path):
    shutil.rmtree(path, ignore_errors=True)

def delete_file_if_exist(path):
  if os.path.exists(path):
    os.remove(path)

def create_fragment_dirs():
    create_dir_if_needed(frag_write_path)

def create_kmer_dirs():
    create_dir_if_needed(kmer_write_path)

def create_circ_dirs():
    create_dir_if_needed(circ_out_path)
    create_dir_if_needed(circ_split_path)

def create_inc_factor_dirs():
    create_dir_if_needed(incfac_out_path)

def create_orit_dirs():
    create_dir_if_needed(orit_out_path)

def create_rrna_dirs():
    create_dir_if_needed(rrna_out_path)
