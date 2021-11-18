# default args
default_threads = 8
default_coverage = 5

# int constants
frag_len = 5000
k = 7
max_frag = 10**6
DIRECTORY_INPUT = 0
FILE_INPUT = 1

# progress bar descriptions
frag_bar_desc  = "fragments             "
kmer_bar_desc =  "kmers                 "
circ_bar_desc =  "circularity           "
gc_bar_desc =    "gc content            "
inc_fac_desc =   "incompatibility factor"
orit_bar_desc =  "orit                  "
rrna_bar_desc =  "rrna                  "

# Databases
db_path = "./biomarker_dbs"

# biomarker tools
default_cmscan_path = "cmscan"
default_blastn_path = "blastn"
default_seq2vec_path = "seq2vec"
default_nucmer_path = "nucmer"

# log files
err_file = "error.txt"
log_file = "log.txt"

# results paths
frag_write_path = "results/fragments"
kmer_write_path = "results/kmers"
circ_write_path = "results/circular"
dataset_path = "results/data.csv"

# temp paths
circ_out_path = "temp/nucmer_out"
circ_split_path = "temp/split"
incfac_out_path = "temp/incfac"
orit_out_path = "temp/orit"
rrna_out_path = "temp/rrna"
