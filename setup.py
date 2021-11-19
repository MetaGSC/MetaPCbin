import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "pipeline",
    version = "0.1.0",
    author="Chamika Nandasiri, Sasindu Alahakoon, Gayal Dassanayake",
    author_email="chamikanandasiri97@gmail.com, dilsharasasindu@gmail.com, \
    g.c.dassanayake@gmail.com",
    description = ("MetaGSC plasmid/chromosome predictor for metagenomic assemblies."),
    keywords = ["bioinformatics", "plasmid", "chromosome", "metagenomic"],
    url = "https://github.com/MetaGSC/pipeline",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    classifiers=[
        'Operating System :: POSIX :: Linux',
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "Natural Language :: English"
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    install_requires=[
        "biopython",
        "tqdm",
        "setuptools",
    ],
    python_requires=">=3.6",
    scripts=[]
)