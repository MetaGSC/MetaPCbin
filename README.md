# MetaPCbin

MetaPCbinflow that takes a user given sequence and outputs the plasmid probability.
<!-- Add more details to explain the tool and its process -->

## Configuration

Can be installed via conda, pip or manually. However conda is recommended as it installs the third 
party dependencies automatically.

### Conda Installation (Recommended)

<!-- To be completed after conda setup -->

All the prerequisites will be installed automatically in the conda environment.

### Pip Installation  

<!-- To be completed after pip setup -->

Pip install will install `tqdm`, `biopython` for you. However `Seq2Vec`, `Infernal`, `Mummer`, 
`Blast+` listed in the dependencies should be installed manually.

### Manual Installation

Need to install all dependencies manually.

## Dependencies

Following tools should be installed before running the software.

-   **Seq2Vec** - used for kmer count
    
-   **Infernal** - used for calculate the rRNA availability
    
-   **Mummer** - used to calculate circularity
    
-   **Blast+** - used for OriT sequence availability and Incompatibility sequence availability

-   **Biopython** - used to read fasta files

-   **tqdm** - used to display runtime progress

### Seq2Vec (kmer count) - [github link](https://github.com/anuradhawick/seq2vec)

In linux,
``` bash
git clone https://github.com/anuradhawick/seq2vec.git
cd seq2vec
mkdir build; cd build; cmake ..; make -j8
```

### Infernal (rRNA) - [github link](https://github.com/EddyRivasLab/infernal)

``` bash
wget eddylab.org/infernal/infernal-1.1.4.tar.gz
tar xf infernal-1.1.4.tar.gz  
cd infernal-1.1.4
./configure
make
make install
cd easel
make install
cmscan
chmod 777  '/infernal-1.1.4/src/cmscan.c'
```

### MUMMER (Circularity) - [documentation link](http://mummer.sourceforge.net/manual/#installation)

``` bash
wget https://downloads.sourceforge.net/project/mummer/mummer/3.23/MUMmer3.23.tar.gz
tar -xvf MUMmer3.23.tar.gz 
cd MUMmer3.23/
sudo apt-get install csh
make check
make install
./nucmer -h
```

### BLAST+ (OriT and Incomp) - [documentation link](https://www.ncbi.nlm.nih.gov/books/NBK569861/)

``` bash
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.7.1/ncbi-blast-2.7.1+-x64-linux.tar.gz
tar zxvpf ncbi-blast-2.7.1+-x64-linux.tar.gz
```

### BIOPYTHON
``` bash
conda install -c conda-forge biopython
```

### TQDM
``` bash
conda install -c conda-forge tqdm
```

> [OPTIONAL] Add the paths of the executables to your system path for tools `seq2vec`, `blastn` 
in BLAST+ `cmscan` in Infernal and `nucmer` in MUMMER.

## Usage

- Use the `pipeline.py` to run the pipeline. The `--help` tag provides a list of all parameters.

```
$ python pipeline.py --help

usage: pipeline.py [-h] [-f FILES [FILES ...]] [-o OUT] [-d DIRECTORY] [-c COVERAGE] [-t THREADS] 
                        [--cmscan CMSCAN] [--blastn BLASTN] [--seq2vec SEQ2VEC] [--nucmer NUCMER]

MetaGSC plasmid/chromosome predictor for metagenomic assemblies.

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        list of input fasta files (default: None)
  -o OUT, --out OUT     output file destination (default: None)
  -d DIRECTORY, --directory DIRECTORY
                        directory of input fasta files (default: None)
  -c COVERAGE, --coverage COVERAGE
                        fragment coverage (default: 5)
  -t THREADS, --threads THREADS
                        number of threads (default: 8)
  --cmscan CMSCAN       path to cmscan (default: cmscan)
  --blastn BLASTN       path to blastn (default: blastn)
  --seq2vec SEQ2VEC     path to seq2vec (default: seq2vec)
  --nucmer NUCMER       path to nucmer (default: nucmer)
```

- It is mandatory to specify either `-f` or `-d`. If both are specified, the `-f` takes precedence.

- The thread count specified by `-t` will be used in using tools to generate features.

- The coverage parameter specified by `-c` specifies the fragment coverage used to break sequences 
into fragments.

- If the `cmscan`, `blastn`, `seq2vec`, `nucmer` executable paths are not added to the system path, 
specify the paths using the `--cmscan`, `--blastn`, `--seq2vec` and `--nucmer` parameters.

- The progress logs will be displayed the console output and in [log.txt](log.txt) file 
along with a timestamp.

- The errors will be displayed the console output and in [error.txt](error.txt) file 
along with a timestamp.

- The kmer files required for the neural network is saved to the [results/kmers](results/kmers) 
directory.

- The biomarker features required for the random forest model is saved to the 
[results/data.csv](results/data.csv) file.

## Output
<!-- To be completed -->
