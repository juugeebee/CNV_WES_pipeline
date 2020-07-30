# Author: Julie BOGOIN

import os
import pandas

#### FUNCTION ####
##################
def family (df, pedigree):
    
    related1 = []
    related2 = []
    lo = []

    for index, row in df.iterrows():

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

    df['related1'] = pandas.Series(related1)
    df['related2'] = pandas.Series(related2)
    df['in_related1'] = False
    df['in_related2'] = False
    df['in_sample'] = True

    for index_p, row_p in pedigree.iterrows():

        index = row_p['Index']
        mother = row_p['Mother']
        father = row_p['Father']

        switch = df[(df['sample'] == index) \
        | (df['sample'] == mother) \
        |(df['sample'] == father) ]
        
        lo.append(switch)
    
    return lo


def overlap (families, df):

    family_list = []
  

    for family in families: 

        family.sort_values(by=['effect','contig', 'start', 'sample'], inplace=True)
        family.reset_index(inplace=True)
        del family['index']

        df_1 = family.shift(periods=1)
        
        family['in_related1'] = (family['effect'] == df_1['effect'])\
                                        & (family['contig'] == df_1['contig'])\
                                        & (family['start'] <= df_1['end']) \
                                        & (family['end'] >= df_1['start']) \
                                        & (family['related1'] == df_1['sample'])

        family['in_related2'] = (family['effect'] == df_1['effect'])\
                                        & (family['contig'] == df_1['contig'])\
                                        & (family['start'] <= df_1['end']) \
                                        & (family['end'] >= df_1['start']) \
                                        & (family['related2'] == df_1['sample'])

        family_list.append(family)

    concat = pandas.concat(family_list, axis=0, ignore_index=True)

    return concat 


def final (concat):
    
    # Creation df final
    final = pandas.DataFrame(columns=['contig','effect', \
    'start', 'end', 'in_sample', 'in_related1', 'in_related2'])
    final['start'] = concat['start']
    final['end'] = concat['end']
    final['contig'] = concat['contig']
    final['effect'] = concat['effect']
    final['in_sample'] = concat['in_sample']
    final['in_related1'] = concat['in_related1']
    final['in_related2'] = concat['in_related2']

    return final


#### MAIN ####
##############
print("\nTransmission program openning.\n")

path = "."
dirs = os.listdir(path)
# Creation df final

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

    if not os.path.exists('./transmission'):
        os.makedirs('./transmission')

    ### CNVKIT    
    family_cnvkit = family(df_cnvkit, pedigree)
    ol_cnvkit = overlap(family_cnvkit, df_cnvkit)
    final_cnvkit = final(ol_cnvkit)

    if os.path.isfile('./transmission/cnvkit_transmission.csv'):
        os.remove('./transmission/cnvkit_transmission.csv')
        print('Previous cnvkit_transmission.csv file removed.')
    
    final_cnvkit.to_csv('transmission/cnvkit_transmission.csv', index=False)                                                                                           
    print("cnvkit_transmission.csv generated.\n")


    ### GATK
    family_gatk = family(df_gatk, pedigree)
    ol_gatk = overlap(family_gatk, df_gatk)
    final_gatk = final(ol_gatk)

    if os.path.isfile('./transmission/gatk_transmission.csv'):
        os.remove('./transmission/gatk_transmission.csv')
        print('Previous gatk_transmission.csv file removed.')
    
    final_gatk.to_csv('transmission/gatk_transmission.csv', index=False)                                                                                           
    print("gatk_transmission.csv generated.\n")


    ### cn.mops
    family_cn = family(df_cnmops, pedigree)
    ol_cn = overlap(family_cn, df_cnmops)
    final_cn = final(ol_cn)

    if os.path.isfile('./transmission/cn_transmission.csv'):
        os.remove('./transmission/cn_transmission.csv')
        print('Previous cn_transmission.csv file removed.')
    
    final_cn.to_csv('transmission/cn_transmission.csv', index=False)                                                                                           
    print("cn_transmission.csv generated.\n")


    ### excavator2
    family_ex = family(df_excavator2, pedigree)
    ol_ex = overlap(family_ex, df_excavator2)
    final_ex = final(ol_ex)

    if os.path.isfile('./transmission/ex_transmission.csv'):
        os.remove('./transmission/ex_transmission.csv')
        print('Previous ex_transmission.csv file removed.')
    
    final_ex.to_csv('transmission/ex_transmission.csv', index=False)                                                                                           
    print("ex_transmission.csv generated.\n")


    ### exomedepth
    family_ed = family(df_exomedepth, pedigree)
    ol_ed = overlap(family_ed, df_exomedepth)
    final_ed = final(ol_ed)

    if os.path.isfile('./transmission/ed_transmission.csv'):
        os.remove('./transmission/ed_transmission.csv')
        print('Previous ed_transmission.csv file removed.')
    
    final_ed.to_csv('transmission/ed_transmission.csv', index=False)                                                                                           
    print("ed_transmission.csv generated.\n")
    
else:
    print('Le fichier pedigree.txt est absent. Calcul impossible.\n')

print("Transmission program job done!\n")