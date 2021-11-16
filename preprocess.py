import os

from fragment import fragment
from constants import *
from helpers import timestamp, print_error

def preprocess(args):
    ''' Preprocess sequences t0 generate kmer, biomarker features
    '''
    files = []
    if(args.files != None and args.directory != None):
        print_error("Either -f or -d are required")
        return -1
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
                print_error(f"{timestamp()} Error listing input directory files: {err}\n")
                return -1
        fragment(files, args.coverage)
        return 0
