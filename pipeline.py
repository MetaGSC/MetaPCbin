import sys
import argparse

from constants import *
from preprocess import preprocess

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

    return parser.parse_args()

def main(args):
    ''' Driver function that preprocesses and feed data to the model
    '''
    ret = preprocess(args)
    # if(ret==0):
        # TODO: call the ML model function here


if __name__ == "__main__":
    args = parse_user_arguements()
    main(args)