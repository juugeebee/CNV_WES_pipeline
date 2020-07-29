# Author: Julie BOGOIN

import os
import pandas

print("\nFrequences program openning.\n")

if os.path.isfile('cnv_with_frequences.txt'):
    os.remove('cnv_with_frequences.csv')
    print('Previous results file removed.')

df = pandas.read_csv('interval_run_results.txt', sep='\t', index_col=False)
df['sample'].astype('str')
df['start'].astype('str').astype('int')
df['end'].astype('str').astype('int')

df_1 = df.shift(periods=1)

df['TF'] = (df['effect'] == df_1['effect'])\
                                    & (df['contig'] == df_1['contig'])\
                                    & (df['start'] < df_1['end']) \
                                    & (df['end'] > df_1['start']) \
                                    & (df['sample'] != df_1['sample'])

df['frequences_in_run'] = 1

tf_list = df['TF'].tolist()
freq_list = df['frequences_in_run'].tolist()

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

df['frequences_in_run'] = pandas.Series(freq_list)
del df['TF']

df.to_csv('cnv_with_frequences.txt', sep='\t', index=False)                                                                                           
print('cnv_with_frequences.txt\n')
print("\nFrequences program job done.\n")

    