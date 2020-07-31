#!/bin/bash

# Author: Julie BOGOIN

source ~/miniconda3/etc/profile.d/conda.sh
conda activate fastq_bam_env

cd /media/Data2/jbogoin/ref

bowtie2  -x hg38_GenDev \
-1 /media/Data2/jbogoin/Test_New_Medexome/13A4276_R1_001.fastq.gz  \
-2 /media/Data2/jbogoin/Test_New_Medexome/13A4276_R2_001.fastq.gz \
-S /media/Data2/jbogoin/Test_New_Medexome/bowtie.sam 

cd /media/Data2/jbogoin/Test_New_Medexome

samtools view -bS bowtie.sam -o bowtie.bam

samtools sort bowtie.bam -o bowtie.sorted.bam

samtools index bowtie.sorted.bam