import os
from Bio import SeqIO

from preprocess.fragment import fragment
from preprocess.kmer import count_kmers
from preprocess.circular import calc_circularity
from preprocess.gc_content import gc_content
from preprocess.inc_fac import calc_inc_factor
from constants import *
from helpers import print_error

def generate_seq_map(files):
    seq_map = {}
    for file in files:
        try:
            for record in SeqIO.parse(file, 'fasta'):
                seq_map[record.id] = {'filepath':file}
        except Exception as err:
            print_error(f"Error reading fasta file {file}: {err}")
    return seq_map

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
                print_error(f"Error listing input directory files: {err}\n")
                return -1

        #kmer count
        frag_count = fragment(files, args.coverage)
        count_kmers(args.seq2vec, args.threads, frag_count)

        #biomarkers
        seq_map = generate_seq_map(files)
        input_mode = DIRECTORY_INPUT if args.directory != None else FILE_INPUT

        calc_circularity(args.nucmer, args.threads, files, seq_map, input_mode)
        gc_content(files, seq_map)
        calc_inc_factor(args.blastn, files, args.threads, seq_map)

        return 0
