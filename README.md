# Team2-GenePrediction

# Gene Prediction
## Pipeline overview
Gene prediction was performed using the combination of GeneMarkS-2 and Prokka. Users have the option to run Prokka or GMS2 individually or to run them together and combine the output. Running Prokka or the combination of Prokka and GMS2 will predict ncRNAs as well as coding sequences. However, running just GMS2 will return coding sequences.

![Pipeline](Images/Intial_1.png)

## Arranging Assembly Output
The input for the main wraper script is the path to a directory containing contigs in fasta format. However, if the contigs are within a sub-directory, where each sub-direcotry is the name for the sample, the arrange_contigs.py script will retreive the contigs files within each sub-directory, rename it to match the sample name, and store a copy in a new directory. This direcotry is then suitable to be used as the input for prokka-gms2-wrapper.py.
Usage:
```
arrange-contigs.py -i /path/to/directory
```
## Predicting genes
Once the input directory has been created (if necessary), the prokka-gms2-wrapper.py script can then be used to predict genes.

### Dependencies
* GeneMarkS-2 : Note, the path to the gms2.pl script must be manually adjusted
* Prokka
* gffcompare
* gffread
* bedtools
All dependencies except GeneMarkS-2 can be installed with conda.

### Input options
```
-i/--input : path to directory containing input contigs in fasta format
-gms2/--GeneMarkS2 : flag to specify to use GMS2 for gene prediction
-pr/--prokka : flag to specify to use Prokka for gene prediction
-c/--combine : flag to specify to use Prokka and GMS2 for gene prediction
-o/--output : name of directory to store outputs, will be created; default = "gene-predictions"
```
### Usage
```
To use GMS2
prokka-gms2-wrapper.py -i /path/to/input_dir --GeneMarkS2 -o output_directory_name
To use Prokka
prokka-gms2-wrapper.py -i /path/to/input_dir --prokka -o output_directory_name
To use both
prokka-gms2-wrapper.py -i /path/to/input_dir --combine -o output_directory_name
```


## Installation

```
## Prokka Installation
conda install -c conda-forge -c bioconda prokka
prokka --setupdb
```
```
## Prodigal Installation
conda install -c conda-forge -c bioconda prodigal
prokka --setupdb
```
```
## GeneMarkS Installation
wget http://topaz.gatech.edu/GeneMark/tmp/GMtool_fhCZT/gms2_linux_64.tar.gz
cp  gmhmmp2_key   ~/.gmhmmp2_key
```
```
## Glimmer Installation
conda install -c bioconda glimmer
```
```
## Balrog Installation
conda create -n balrog_env python=3.7
conda activate balrog_env
conda install -c conda-forge -c bioconda balrog mmseqs2
conda install -c pytorch pytorch torchvision torchaudio cpuonly
```
```
## MetaGeneAnnotator Installation
wget metagene.nig.ac.jp/metagene/mga_x86_64.tar.gz
tar xzf mga_x86_64.tar.gz
```
## Abintio Based Gene Prediction Tools

## with Prokka
Prokka is a command-line-based rapid annotation tool developed by the University of Melbourne bioinformatician Torsten Seemann, which is very convenient and fast to annotate small genomes such as bacteria and viruses. Prokka can fully annotate a draft bacterial genome in about 10 minutes on a typical desktop computer. It produces standards-compliant output files for further analysis or viewing in a genome browser. To use Prokka, prepare fasta format file that needs to be annotated.

The command used was
```
prokka <assembly.fasta> --outdir <output/path/> --kingdom Bacteria --rfam
```
## with Prodigal
The command used was
```
prodigal -i <output/path/assembly.fasta> -o <output/path/output.gff> --output_format --output_format gff
```
## with Glimmer3
The command used was
```
build-icm [options] output_file < input-file
glimmer3 seq.fna output_file.icm result
#output will give two files: result.predict (gff file) and result.detail which lists out all the genes
```
## with GeneMarkS
The command used was
```
gms2.pl -s <sequence.fasta> --genome-type <TYPE (bacteria/archae/auto)> --output <Output.gff>

```
## with balrog
The command used was
```
balrog -i <sequence.fasta> -o <out.gff>
```
## with MetaGeneAnnotator
The command used was
```
mga <sequence.fasta> -s > out.txt
# To convert to gff3 (Tentative, not necessarily correct)
awk -v OFS='\t' -e 'BEGIN{print("##gff-version 3")}{if($1 ~ "#"){print($0)}else{print($1, "MetaGeneAnnotator", "CDS", $2, $3, $7, $4, $5, $6";"$8)}}' out.txt > out.gff
```

## Homology Based Gene Prediction Tools

## with BLAT
The command used was
```
blat </path/to/reference.fna> </path/to/contigs.fasta> -out=psl <blat.psl.out>

```

## Gene Prediction Results
ORForise was used to assess each of the above tools' Gene Prediction Accuracy.Combining tools improves detection, but increases the False Discovery Rate - FP/(FP+TP).

![Pipeline](Images/Results.png)

Finally,the Prodigal/GMS2 combination was chosen because to its low False Discovery Rate.

GFFcompare and bedtools are used to identify common and unique genes in (Prodigal and GMS2) and to quantify sensitivty and precision.

Combine predicted coding genes and noncoding genes into a final file (FNA,FAA,GFF).

### Final Pipeline
![Pipeline](Images/Final.png)


## References

. Nicholas J Dimonaco, Wayne Aubrey, Kim Kenobi, Amanda Clare, Christopher J Creevey, No one tool to rule them all: prokaryotic gene prediction tool annotations are highly dependent on the organism of study, Bioinformatics, Volume 38, Issue 5, 1 March 2022, Pages 1198–1207​

. John Besemer, Alexandre Lomsadze, Mark Borodovsky, GeneMarkS: a self-training method for prediction of gene starts in microbial genomes. Implications for finding sequence motifs in regulatory regions, Nucleic Acids Research, Volume 29, Issue 12, 15 June 2001, Pages 2607–2618,​

. Torsten Seemann, Prokka: rapid prokaryotic genome annotation, Bioinformatics, Volume 30, Issue 14, 15 July 2014, Pages 2068–2069​

. Markus J Sommer, Steven L Salzberg, Balrog: A universal protein model for prokaryotic gene prediction, PLoS Computational Biology, Volume 17, 26 February 2021, e1008727​

. Hideki Noguchi, Takeaki Taniguchi, Takehiko Itoh, MetaGeneAnnotator: Detecting Species-Specific Patterns of Ribosomal Binding Site for Precise Gene Prediction in Anonymous Prokaryotic and Phage Genomes, DNA Research, Volume 15, Issue 6, 21 October 2008, Pages 387-396

