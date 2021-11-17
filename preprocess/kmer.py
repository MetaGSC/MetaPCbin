import subprocess as sp

from progress_bar import *
from helpers import create_kmer_dirs, print_error, print_log
from constants import *
import os

def count_kmers(seq2vec_path, threads, frag_count):
    ''' Generates the kmer counts for each fragment using seq2vec
    '''
    try:
        print_log("Generating kmer counts...")
        create_kmer_dirs()
        progress_bar = create_visual_progress_bar(sum(frag_count.values()), kmer_bar_desc)
        for filename in os.listdir(frag_write_path):
            name = os.path.splitext(os.path.basename(filename))[0]
            frag_file = os.path.join(frag_write_path, filename)
            write_file = os.path.join(kmer_write_path, name)
            args = [
                seq2vec_path,
                '-f', str(frag_file),
                '-o', str(write_file),
                '-t', str(threads),
                '-k', str(k),
            ]
            sp.run(args, stdout=sp.PIPE, stderr=sp.PIPE)

            update_val = frag_count[name] if name in frag_count.keys() else 0
            update_progress_bar(progress_bar, update_val)

        close_progress_bar(progress_bar)
    except Exception as err:
        print_error(f"Error generating kmer counts: {err}")

    print_log("Generating kmer counts completed.")
