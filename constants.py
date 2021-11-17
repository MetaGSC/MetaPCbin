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

# temp paths
circ_out_path = "temp/nucmer_out"
circ_split_path = "temp/split"
incfac_out_path = "temp/incfac"

# # rrna files
# plas_rrna_write_path = "results/plasmid/Data/rrna"
# chrom_rrna_write_path = "results/chromosome/Data/rrna"
# ex_plas_rrna_write_path = "results/extra-plasmid/Data/rrna"

# plas_rrna_out_path = "results/plasmid/extra/rrna-out"
# chrom_rrna_out_path = "results/chromosome/extra/rrna-out"
# ex_plas_rrna_out_path = "results/extra-plasmid/extra/rrna-out"

# # orit files
# plas_orit_out_path = "results/plasmid/extra/orit-out"
# chrom_orit_out_path = "results/chromosome/extra/orit-out"
# ex_plas_orit_out_path = "results/extra-plasmid/extra/orit-out"

# plas_orit_write_path = "results/plasmid/Data/orit"
# chrom_orit_write_path = "results/chromosome/Data/orit"
# ex_plas_orit_write_path = "results/extra-plasmid/Data/orit"
