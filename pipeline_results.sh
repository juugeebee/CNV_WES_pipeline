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

python ~/CNV_WES_pipeline/cnv_results.py
python ~/CNV_WES_pipeline/cnv_interval_objet_sample.py
python ~/CNV_WES_pipeline/cnv_interval_objet_run.py

python ~/CNV_WES_pipeline/frequences.py

conda deactivate

# annotations

# annovar
conda activate annot_env

bash ~/CNV_WES_pipeline/annovar.sh

conda deactivate

conda activate results_cnv

cd annovar_output
python ~/CNV_WES_pipeline/annovar_results.py

# ClinVar
# In_gene
# DGV_count

cd $DATA
python ~/CNV_WES_pipeline/combine_annot.py

conda deactivate

echo ""
echo "+++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++++++"
echo "pipeline_results.sh job done!"
echo "+++++++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++++++"
echo ""