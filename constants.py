default_threads = 8
default_coverage = 5
# batch_size = 1000
frag_len = 5000
k = 7
err_file = "error.txt"
log_file = "log.txt"

max_frag = 10**6
# chrom_max = 10**6
# ex_plas_max = 10**5

# progress bar descriptions
frag_bar_desc  = "fragments "

# # sequence filter constants
# plas_filter_val = 0.99
# chrom_filter_val = 0.01
# plas_filter_file = "/media/gayal/Programming/FYP/databases/DNAML-plasmid.fasta.probs.out"
# chrom_filter_file = "/media/gayal/Programming/FYP/databases/DNAML_bacterial_batch0.fasta.probs.out"

# Databases
# plas_db_path = "/media/gayal/Programming/FYP/databases/DNA-ML_FYP_2021/plasmid_refs"
# chrom_db_path = '/media/gayal/Programming/FYP/databases/DNA-ML_FYP_2021/bacterial_references'
# plas_db_path = "/media/gayal/Programming/FYP/databases/DNA-ML_FYP_2021/plas-ref-small"
# chrom_db_path = '/media/gayal/Programming/FYP/databases/DNA-ML_FYP_2021/bact-ref-tiny'
db_path = "../../references/biomarkerdbs"
cmscan_path = "cmscan"
blastn_path = "blastn"
seq2vec_path = "seq2vec"
nucmer_path = "nucmer"

# # label files 
# plas_label_path = "results/plasmid/Label"
# chrom_label_path = "results/chromosome/Label"
# ex_plas_label_path = "results/extra-plasmid/Label"

# # target csv files
# plas_target_path = "results/plasmid/target.csv"
# chrom_target_path = "results/chromosome/target.csv"
# ex_plas_target_path = "results/extra-plasmid/target.csv"

frag_write_path = "results/fragments"

# # seq target csv files
# seq_plas_target_path = "results/plasmid/seq_target.csv"
# seq_chrom_target_path = "results/chromosome/seq_target.csv"
# seq_ex_plas_target_path = "results/extra-plasmid/seq_target.csv"

# # seq fragment files
# seq_plas_write_path = "results/plasmid/Data/seq"
# seq_chrom_write_path = "results/chromosome/Data/seq"
# seq_extra_plasmid_write_path = "results/extra-plasmid/Data/seq"

# # fragment txt files
# plas_txt_write_path = "results/plasmid/extra/frag-txt"
# chrom_txt_write_path = "results/chromosome/extra/frag-txt"
# extra_plasmid_txt_write_path = "results/extra-plasmid/extra/frag-txt"

# # kmer files

# plas_7mer_write_path = "results/plasmid/Data/7mers"
# chrom_7mer_write_path = "results/chromosome/Data/7mers"
# ex_plas_7mer_write_path = "results/extra-plasmid/Data/7mers"

# # circularity files
# plas_circ_write_path = "results/plasmid/Data/circular"
# chrom_circ_write_path = "results/chromosome/Data/circular"
# ex_plas_circ_write_path = "results/extra-plasmid/Data/circular"

# plas_circ_out_path = "results/plasmid/extra/nucmer_out"
# chrom_circ_out_path = "results/chromosome/extra/nucmer_out"
# ex_plas_circ_out_path = "results/extra-plasmid/extra/nucmer_out"

# plas_frag_split_path = "results/plasmid/extra/split"
# chrom_frag_split_path = "results/chromosome/extra/split"
# ex_plas_frag_split_path = "results/extra-plasmid/extra/split"

# # inc factor files
# plas_inc_out_path = "results/plasmid/extra/inc-out"
# chrom_inc_out_path = "results/chromosome/extra/inc-out"
# ex_plas_inc_out_path = "results/extra-plasmid/extra/inc-out"

# plas_inc_write_path = "results/plasmid/Data/inc-fac"
# chrom_inc_write_path = "results/chromosome/Data/inc-fac"
# ex_plas_inc_write_path = "results/extra-plasmid/Data/inc-fac"

# # rrna files
# plas_rrna_write_path = "results/plasmid/Data/rrna"
# chrom_rrna_write_path = "results/chromosome/Data/rrna"
# ex_plas_rrna_write_path = "results/extra-plasmid/Data/rrna"

# plas_rrna_out_path = "results/plasmid/extra/rrna-out"
# chrom_rrna_out_path = "results/chromosome/extra/rrna-out"
# ex_plas_rrna_out_path = "results/extra-plasmid/extra/rrna-out"

# # gc-content files
# plas_gccontent_write_path = "results/plasmid/Data/gccontent"
# chrom_gccontent_write_path = "results/chromosome/Data/gccontent"
# ex_plas_gccontent_write_path = "results/extra-plasmid/Data/gccontent"

# # orit files
# plas_orit_out_path = "results/plasmid/extra/orit-out"
# chrom_orit_out_path = "results/chromosome/extra/orit-out"
# ex_plas_orit_out_path = "results/extra-plasmid/extra/orit-out"

# plas_orit_write_path = "results/plasmid/Data/orit"
# chrom_orit_write_path = "results/chromosome/Data/orit"
# ex_plas_orit_write_path = "results/extra-plasmid/Data/orit"

# # mobilization, conjugation, replication files
# plas_mob_out_path = "results/plasmid/extra/mob-out" 
# chrom_mob_out_path = "results/chromosome/extra/mob-out" 
# ex_plas_mob_out_path = "results/extra-plasmid/extra/mob-out" 

# plas_rep_out_path = "results/plasmid/extra/rep-out" 
# chrom_rep_out_path = "results/chromosome/extra/rep-out" 
# ex_plas_rep_out_path = "results/extra-plasmid/extra/rep-out" 

# plas_con_out_path = "results/plasmid/extra/con-out" 
# chrom_con_out_path = "results/chromosome/extra/con-out" 
# ex_plas_con_out_path = "results/extra-plasmid/extra/con-out" 

# plas_mob_write_path = "results/plasmid/Data/mobilization" 
# chrom_mob_write_path = "results/chromosome/Data/mobilization"
# ex_plas_mob_write_path = "results/extra-plasmid/Data/mobilization" 

# plas_rep_write_path = "results/plasmid/Data/replication" 
# chrom_rep_write_path = "results/chromosome/Data/replication"
# ex_plas_rep_write_path = "results/extra-plasmid/Data/replication" 

# plas_con_write_path = "results/plasmid/Data/conjugation" 
# chrom_con_write_path = "results/chromosome/Data/conjugation"
# ex_plas_con_write_path = "results/extra-plasmid/Data/conjugation" 
