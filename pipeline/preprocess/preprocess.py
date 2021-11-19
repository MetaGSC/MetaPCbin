import os
from Bio import SeqIO

from pipeline.preprocess.fragment import fragment
from pipeline.preprocess.kmer import count_kmers
from pipeline.preprocess.circular import calc_circularity
from pipeline.preprocess.gc_content import gc_content
from pipeline.preprocess.inc_fac import calc_inc_factor
from pipeline.preprocess.orit import calc_orit
from pipeline.preprocess.rrna import calc_rrna
from pipeline.preprocess.write_dataset import write_dataset
from pipeline.constants import *
from pipeline.helpers import print_error

def generate_seq_map(files):
    seq_map = {}
    for file in files:
        try:
            for record in SeqIO.parse(file, 'fasta'):
                seq_map[record.id] = {'filepath':file}
        except Exception as err:
            print_error(f"Error reading fasta file {file}: {err}")
    return seq_map

def preprocess(args, files):
    ''' Preprocess sequences t0 generate kmer, biomarker features
    '''
    #kmer count
    frag_count = fragment(files, args.coverage)
    count_kmers(args.seq2vec, args.threads, frag_count)

    #biomarkers
    seq_map = generate_seq_map(files)
    input_mode = DIRECTORY_INPUT if args.directory != None else FILE_INPUT

    calc_circularity(args.nucmer, args.threads, files, seq_map, input_mode)
    gc_content(files, seq_map)
    calc_inc_factor(args.blastn, files, args.threads, seq_map)
    calc_orit(args.blastn, files, args.threads, seq_map)
    calc_rrna(args.cmscan, files, args.threads, seq_map)
    write_dataset(seq_map)

    return 0
