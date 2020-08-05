# Author: Julien BURATTI

source ~/miniconda3/etc/profile.d/conda.sh
conda activate fastq_bam_env

echo ""
echo "fastq_to_bam.sh start"
echo ""

REF="/media/Data1/jbogoin/ref/hg38_Mlast/hg38_GenDev.fa"
DATA=$PWD

### REMOVE previous dedup.bam files ###
rm -f *.bam*

## MAPPING BWA SEQUENTIAL 
for R1 in *_R1_*.fastq.gz; 
    
    do 
    R2=${R1/_R1_/_R2_}; 

    SAMPLE=${R1%%_*};

    cd /media/Data2/jbogoin/ref;

    bowtie2 -p 36 -x hg38_GenDev -1 $DATA/$R1 -2 $DATA/$R2 -S $DATA/$SAMPLE.sam;

    cd $DATA

    samtools view -@ 36 -bS $SAMPLE.sam -o $SAMPLE.bam;

    samtools sort -@ 36 $SAMPLE.bam -o $SAMPLE.sorted.bam;

    #samtools index -@ 12 $SAMPLE.sorted.bam;

done

### MARK DUPLICATES
for i in *sorted.bam; 
    
    do 
    SAMPLE=${i%.*};
 
    sambamba markdup -t 36 ${SAMPLE}.bam ${SAMPLE}.dedup.bam;
    
done

echo ""
echo "fastq_to_bam.sh job done!"
echo ""
