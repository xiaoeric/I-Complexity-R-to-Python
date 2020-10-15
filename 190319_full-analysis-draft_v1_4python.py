from typing import Dict
import pandas as pd

# dataset is a dictionary of DataFrames
# consider instead merging all DataFrames and labelling each word with its associated language?
dataset: Dict[str, pd.DataFrame] = {}

# (1.1.1) Cleaning
# (1.1.1.1) Clean up '----' in Hungarian entries
dataset['hun.txt'] = dataset['hun.txt'][dataset['hun.txt']['V3'] != '----']
# (1.1.1.2) Delete space in front of ' N;SG;NDEF' in Tajik entries
dataset['tgk.txt']['V3'].replace('^ ', '', inplace=True, regex=True)
# (1.1.1.3) Replace 'ADJ/GEN' with 'ADJ;GEN' in Armenian entries
dataset['xcl.txt']['V3'].replace('ADJ/GEN', 'ADJ;GEN', inplace=True)  # what is fixed=T in the original code?
# (1.1.1.4) Replace 'AJD' with 'ADJ' in Armenian entries
dataset['xcl.txt']['V3'].replace('AJD', 'ADJ', inplace=True)
# (1.1.1.5) Replace 'PCTP' with 'PTCP' in Slovenian entries
dataset['slv.txt']['V3'].replace('PCTP', 'PTCP', inplace=True)

# (3.1.2.1.1) Fixing Adyghe
# why do we use .n for this code segment in the original code?
dataset['ady.txt']['V3'].replace('N;ERG;PL;DEF;DEF', 'N;INS;PL;DEF', inplace=True)
dataset['ady.txt']['V3'].replace('N;ERG;PL;DEF;NDEF', 'N;INS;PL;NDEF', inplace=True)
dataset['ady.txt']['V3'].replace('N;ERG;SG;DEF;DEF', 'N;INS;SG;DEF', inplace=True)
dataset['ady.txt']['V3'].replace('N;ERG;SG;DEF;NDEF', 'N;INS;SG;NDEF', inplace=True)

# (3.1.4.2) 'ces.txt'
dataset['ces.txt'].loc[dataset['ces.txt']['V3'].str.contains(';ANIM;'), 'V1'] = dataset['ces.txt']['V1'] + '-ANIM'
dataset['ces.txt'].loc[dataset['ces.txt']['V3'].str.contains(';INAN;'), 'V1'] = dataset['ces.txt']['V1'] + '-INAN'
dataset['ces.txt']['V3'].replace(';ANIM;', ';', inplace=True)
dataset['ces.txt']['V3'].replace(';INAN;', ';', inplace=True)

# (3.1.4.5) 'rus.txt'
temp_anim = dataset['rus.txt'][dataset['rus.txt']['V3'] in ['N;ACC;ANIM;SG', 'N;ACC;ANIM;PL']]
temp_anim = dataset['rus.txt'][dataset['rus.txt']['V1'] in temp_anim['V1'].unique()]
temp_inan = dataset['rus.txt'][dataset['rus.txt']['V3'] in ['N;ACC;INAN;SG', 'N;ACC;INAN;PL']]
temp_inan = dataset['rus.txt'][dataset['rus.txt']['V1'] in temp_inan['V1'].unique()]
# is this supposed to just exclude from inan or also from anim?
temp_other = dataset['rus.txt'][dataset['rus.txt']['V1'] not in temp_inan['V1'].unique()]

temp_anim['V1'] = temp_anim['V1'] + '-ANIM'
temp_anim = temp_anim[not temp_anim['V3'].str.contains(';INAN;')]
temp_anim['V3'].replace(';ANIM;', ';', inplace=True)

temp_inan['V1'] = temp_inan['V1'] + '-INAN'
temp_inan = temp_inan[not temp_inan['V3'].str.contains(';ANIM;')]
temp_inan['V3'].replace(';INAN;', ';', inplace=True)

dataset['rus.txt'] = pd.concat([temp_anim, temp_inan, temp_other])
dataset['rus.txt'].sort_values(by='V1', inplace=True)
