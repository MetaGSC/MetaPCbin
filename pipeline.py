import sys
import argparse

from constants import *
from helpers import delete_dir_if_exist
from preprocess.preprocess import preprocess

def parse_user_arguements():
    parser = argparse.ArgumentParser(
        description='MetaGSC plasmid/chromosome predictor for metagenomic assemblies.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument(
        '-f','--files', help='list of input fasta files', 
        required=False, nargs='+'
        )
    parser.add_argument(
        '-o','--out', help='output file', 
        required=False, type=str
        )
    parser.add_argument(
        '-d','--directory', help='directory of input fasta files', 
        required=False, type=str
        )
    parser.add_argument(
        '-c','--coverage', help='fragment coverage', 
        required=False, type=int, default=default_coverage
        )
    parser.add_argument(
        '-t','--threads', help='number of threads', 
        required=False, type=int, default=default_threads
        )
    parser.add_argument(
        '--cmscan', help='path to cmscan', 
        required=False, type=str, default=default_cmscan_path
        )
    parser.add_argument(
        '--blastn', help='path to blastn', 
        required=False, type=str, default=default_blastn_path
        )
    parser.add_argument(
        '--seq2vec', help='path to seq2vec', 
        required=False, type=str, default=default_seq2vec_path
        )
    parser.add_argument(
        '--nucmer', help='path to nucmer',
        required=False, type=str, default=default_nucmer_path
        )

    return parser.parse_args()

def reset_env():
    ''' Clears temporary files of previous runs
    '''
    delete_dir_if_exist(all_results_path)
    delete_dir_if_exist(all_temp_path)

def main(args):
    ''' Driver function that preprocesses and feed data to the model
    '''
    reset_env()
    ret = preprocess(args)
    # if(ret==0):
        # TODO: call the ML model function here


if __name__ == "__main__":
    args = parse_user_arguements()
    main(args)
