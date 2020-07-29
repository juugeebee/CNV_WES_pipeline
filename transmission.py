# Author: Julie BOGOIN

import os
import pandas

print("\nTransmission program openning.\n")

def overlap (df, pedigree):

    trans = pandas.DataFrame(columns=['start', 'end', 'sample', \
        'related1', 'related2', 'in_sample', 'in_related1', 'in_related2'])

    trans['start'] = df['start']
    trans['end'] = df['end']
    trans['sample'] = df['sample']
    trans['contig'] = df['contig']
    trans['effect'] = df['effect']
    trans['in_sample'] = True

    related1 = []
    related2 = []

    for index, row in trans.iterrows():

        for index_p, row_p in pedigree.iterrows():

            if row['sample'] == row_p['Index'] :

                related1.append(row_p['Mother'])
                related2.append(row_p['Father'])

            if row['sample'] == row_p['Mother'] :

                related1.append(row_p['Index'])
                related2.append(row_p['Father'])

            if row['sample'] == row_p['Father'] :

                related1.append(row_p['Mother'])
                related2.append(row_p['Index'])

    trans['related1'] = pandas.Series(related1)
    trans['related2'] = pandas.Series(related2)

    trans['start'].astype('str').astype('int')
    trans['end'].astype('str').astype('int')

    trans.sort_values(by=['effect','contig', 'start', 'sample'], inplace=True)
    trans.reset_index(inplace=True)
    del trans['index']

    df_1 = trans.shift(periods=1)

    trans['in_related1'] = (trans['effect'] == df_1['effect'])\
                                    & (trans['contig'] == df_1['contig'])\
                                    & (trans['start'] <= df_1['end']) \
                                    & (trans['end'] >= df_1['start']) \
                                    & (trans['related1'] == df_1['sample'])

    trans['in_related2'] = (trans['effect'] == df_1['effect'])\
                                    & (trans['contig'] == df_1['contig'])\
                                    & (trans['start'] <= df_1['end']) \
                                    & (trans['end'] >= df_1['start']) \
                                    & (trans['related2'] == df_1['sample'])

    trans.query('in_related1==True and in_related2==True', inplace=True)

    return (trans)


#### MAIN ####
##############


path = "."
dirs = os.listdir(path)

if os.path.isfile('pedigree.txt'):
    pedigree = pandas.read_csv('pedigree.txt', sep='\t',index_col=None, header=[0])
    del pedigree['Comment']
    del pedigree['Sex']
    del pedigree['Fam']

    for directory in dirs:
    
        if directory == 'gatkcnv_output':
            file_path = './' + directory + '/gatk_results.csv'
            if os.path.isfile(file_path):
                df_gatk = pandas.read_csv(file_path,index_col=None)
    
        if directory == 'cnvkit_output':
            file_path = './' + directory + '/cnvkit_results.csv'
            if os.path.isfile(file_path):
                df_cnvkit = pandas.read_csv(file_path,index_col=None)
        
        if directory == 'exomedepth_output':
            file_path = './' + directory + '/exomedepth_results.csv'
            if os.path.isfile(file_path):
                df_exomedepth = pandas.read_csv(file_path,index_col=None)
        
        if directory == 'cn.mops_output':
            file_path = './' + directory + '/cn.mops_results.csv'
            if os.path.isfile(file_path):
                df_cnmops = pandas.read_csv(file_path,index_col=None)
        
        if directory == 'excavator2_output':
            file_path = './' + directory + '/excavator2_results.csv'
            if os.path.isfile(file_path):
                df_excavator2 = pandas.read_csv(file_path,index_col=None)

    ol_gatk = overlap(df_gatk, pedigree)
    ol_cnvkit = overlap(df_cnvkit, pedigree)
    ol_exomedepth = overlap(df_exomedepth, pedigree)
    ol_cnmops = overlap(df_cnmops, pedigree)
    ol_excavator2 = overlap(df_excavator2, pedigree)

    print('Results GATK')
    print(ol_gatk)
    print('\nResults CNVkit')
    print(ol_cnvkit)
    print('\nResults ExomeDepth')
    print(ol_exomedepth)
    print('\nResults cn.mops')
    print(ol_cnmops)
    print('\nResults EXCAVATOR2')
    print(ol_excavator2)

else:
    print('Le fichier pedigree.txt est absent. Calcul impossible.')

print("\nTransmission program job done!\n")




