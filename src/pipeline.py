import os
import argparse

from constants import *
from helpers import delete_dir_if_exist, print_error
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
        '-o','--out', help='output file destination', 
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

def validate_args(args):
    ''' Validates if either -f or -d is provided. Returns the list of input files
    '''
    files = []
    if(args.files == None and args.directory == None):
        print_error("Error: Either -f or -d are required")
        return -1, files
    else:
        if(args.files != None):
            # if a series of input files(-f) is specified
            files = args.files
        else:
            # if an input directory(-d) is specified
            try:
                files = os.listdir(args.directory)
                files = [os.path.join(args.directory, file) for file in files]
            except Exception as err:
                print_error(f"Error listing input directory files: {err}")
                return -1, files
    return 0, files

def main(args):
    ''' Driver function that preprocesses and feed data to the model
    '''
    reset_env()
    ret, files = validate_args(args)
    if(ret == 0):
        ret = preprocess(args, files)
        # if(ret==0):
            # TODO: call the ML model function here

if __name__ == "__main__":
    args = parse_user_arguements()
    main(args)
