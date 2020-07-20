# Author: Julie BOGOIN

source ~/miniconda3/etc/profile.d/conda.sh
conda activate cnvkit_env

for cns_files in *dedup.cns; 
do SAMPLE=${cns_files%%.dedup.cns};

~/cnvkit/cnvkit.py call $cns_files \
    -y -m threshold \
    -t=-1.1,-0.4,0.3,0.7 \
    -o $SAMPLE.new.call.cns;

done

