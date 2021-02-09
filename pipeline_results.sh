#!/bin/bash

# Author: Julie BOGOIN

echo ""
echo "++++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++"
echo "pipeline_results.sh start."
echo "++++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++"
echo ""

DATA=$PWD

source ~/miniconda3/etc/profile.d/conda.sh

### results summary

conda activate results_cnv

python ~/SCRIPTS/CNV_WES_pipeline/cnv_results.py
python ~/SCRIPTS/CNV_WES_pipeline/cnv_interval_objet_sample.py
python ~/SCRIPTS/CNV_WES_pipeline/cnv_interval_objet_run.py

python ~/SCRIPTS/CNV_WES_pipeline/frequences.py

conda deactivate

# annotations

# annovar
conda activate annot_env

bash ~/SCRIPTS/CNV_WES_pipeline/annovar.sh

conda deactivate

conda activate results_cnv

cd annovar_output
python ~/SCRIPTS/CNV_WES_pipeline/annovar_results.py

# ClinVar
# In_gene
# DGV_count

cd $DATA
python ~/SCRIPTS/CNV_WES_pipeline/combine_annot.py

conda deactivate

echo ""
echo "+++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++++++"
echo "pipeline_results.sh job done!"
echo "+++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++++++"
echo ""