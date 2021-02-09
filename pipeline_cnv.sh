#!/bin/bash

# Author: Julie BOGOIN

exec &> cnv_sortie.log

echo ""
echo "++++++++++++++++++++++"
echo "++++++++++++++++++++++"
echo "pipeline_cnv.sh start."
echo "++++++++++++++++++++++"
echo "++++++++++++++++++++++"
echo ""

DATA=$PWD

source ~/miniconda3/etc/profile.d/conda.sh

# sex determination
conda activate sex_env

python3 ~/SCRIPTS/CNV_WES_pipeline/sex_determination.py

conda deactivate

# generation des listes hommes et femmes
conda activate results_cnv

python3 ~/SCRIPTS/CNV_WES_pipeline/female_male_lists.py

conda deactivate

# tools cnv detection
bash ~/SCRIPTS/CNV_WES_pipeline/cn.mops_launch.sh

bash ~/SCRIPTS/CNV_WES_pipeline/cnvkit_detection.sh
cd all
sudo bash ~/SCRIPTS/CNV_WES_pipeline/cnvkit_call.sh
cd cnvkit_output/female
sudo bash ~/SCRIPTS/CNV_WES_pipeline/cnvkit_call.sh
cd ../male
sudo bash ~/SCRIPTS/CNV_WES_pipeline/cnvkit_call.sh
cd ../..

bash ~/SCRIPTS/CNV_WES_pipeline/excavator2_detection.sh

bash ~/SCRIPTS/CNV_WES_pipeline/exomedepth_launch.sh

bash ~/SCRIPTS/CNV_WES_pipeline/gatk_detection.sh

# tools results generation
conda activate results_cnv

cd cn.mops_output
python ~/SCRIPTS/CNV_WES_pipeline/cn.mops_results.py

cd ../cnvkit_output
python ~/SCRIPTS/CNV_WES_pipeline/cnvkit_results.py

cd ../excavator2_output
python ~/SCRIPTS/CNV_WES_pipeline/excavator2_results.py

cd ../exomedepth_output
python ~/SCRIPTS/CNV_WES_pipeline/exomedepth_results.py

cd ../gatkcnv_output
python ~/SCRIPTS/CNV_WES_pipeline/gatk_results.py

cd $DATA

# results summary
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
echo "+++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++"
echo "pipeline_cnv.sh job done!"
echo "+++++++++++++++++++++++++"
echo "+++++++++++++++++++++++++"
echo ""

