#!/bin/bash

# Author: Julie BOGOIN

echo ""
echo "results_launch.sh start"
echo ""

# DATA=$PWD

# source ~/miniconda3/etc/profile.d/conda.sh

# tools results generation

# conda activate results_cnv

# cd cn.mops_output
# python ~/CNV_WES_pipeline/cn.mops_results.py

# cd ../cnvkit_output
# python ~/CNV_WES_pipeline/cnvkit_results.py

# cd ../excavator2_output
# python ~/CNV_WES_pipeline/excavator2_results.py

# cd ../exomedepth_output
# python ~/CNV_WES_pipeline/exomedepth_results.py

# cd ../gatkcnv_output
# python ~/CNV_WES_pipeline/gatk_results.py

# cd $DATA

# # # results summary
python ~/CNV_WES_pipeline/cnv_results.py
python ~/CNV_WES_pipeline/cnv_interval_objet_sample.py
python ~/CNV_WES_pipeline/cnv_interval_objet_run.py

python ~/CNV_WES_pipeline/frequences.py

# annotations

# annovar
 conda activate annot_env

bash ~/CNV_WES_pipeline/annovar.sh

conda activate results_cnv

cd annovar_output
python ~/CNV_WES_pipeline/annovar_results.py

# ClinVar
# In_gene
# DGV_count

cd $DATA
python ~/CNV_WES_pipeline/combine_annot.py

echo ""
echo "results_launch.sh job done!"
echo ""
