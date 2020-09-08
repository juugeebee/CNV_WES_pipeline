# Author: Julie BOGOIN

import os
import pandas

print("\nFrequences program openning.\n")

if os.path.isfile('cnv_with_frequences.txt'):
    os.remove('cnv_with_frequences.txt')
    print('Previous results file removed.')

df_prev = pandas.read_csv('interval_run_results.txt', sep='\t', index_col=False)
df_prev.drop_duplicates(subset=['start', 'end', 'sample'],\
        keep='first', inplace=True)

df_prev['sample'].astype('str')
df_prev['start'].astype('str').astype('int')
df_prev['end'].astype('str').astype('int')

df_curr = df_prev.shift(periods=1)

df_prev['TF'] = (df_prev['effect'] == df_curr['effect'])\
        & (df_prev['contig'] == df_curr['contig'])\
        & (df_curr['start'] <= df_prev['end']) \
        & (df_curr['end'] >= df_prev['start']) \
        & (df_prev['sample'] != df_curr['sample'])

df_prev['frequences_in_run'] = 1
freq_list = df_prev['frequences_in_run'].tolist()

tf_list = df_prev['TF'].tolist()

comp = 0
start = 0
stop = 0

for i in range(len(tf_list)-1):
    
    if (tf_list[i] == False) & (tf_list[i+1] == True) :
        comp = comp + 1
        start = i

    if (tf_list[i] == True) & (tf_list[i+1] == True) :
        comp = comp + 1
    
    if (tf_list[i] == True) & (tf_list[i+1] == False) :
        end = i
        for j in range(start, end):
            freq_list[j] = comp
        comp = 0

df_prev['frequences_in_run'] = pandas.Series(freq_list)
del df_prev['TF']

df_prev.to_csv('cnv_with_frequences.txt', sep='\t', index=False)                                                                                           
print('cnv_with_frequences.txt generated.')
print("\nFrequences program job done.\n")

    