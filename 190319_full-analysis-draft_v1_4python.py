from typing import Dict
import pandas as pd


# TODO
def read():
    pass


def separate_word_classes(dataset: Dict[str, pd.DataFrame]):
    # (2.1) Nouns
    dataset_n = dataset
    # is i (now called lang) here the word or the language? assuming language for now
    for lang in dataset_n.keys():
        print('nouns: ', lang)  # what does collapse mean here?
        dataset_n[lang] = dataset_n[dataset_n[lang].V3.str.contains('^N[[:punct:]]', regex=True)]

    # (2.1.1) remove empty data frames
    for lang in dataset_n:
        if dataset_n[lang].empty:
            del dataset_n[lang]
    # what is langs.nouns and where did it come from

    # (2.2) Verbs
    dataset_v = dataset
    for lang in dataset_v.keys():
        print('verbs: ', lang)
        dataset_v[lang] = dataset_v[dataset_v[lang].V3.str.contains('^V[[:punct:]]', regex=True)]

    # (2.2.1) remove empty data frames
    for lang in dataset_v:
        if dataset_v[lang].empty:
            del dataset_v[lang]

    # (2.3) Adjectives
    dataset_a = dataset
    for lang in dataset_a.keys():
        print('adjectives: ', lang)
        dataset_a[lang] = dataset_a[dataset_a[lang].V3.str.contains('^ADJ[[:punct:]]', regex=True)]

    # (2.3.1) remove empty data frames
    for lang in dataset_a:
        if dataset_a[lang].empty:
            del dataset_a[lang]

    return dataset_n, dataset_v, dataset_a


# dataset is a dictionary of DataFrames
# consider instead merging all DataFrames and labelling each word with its associated language?
# all changes done to dataset_n are not reflected in dataset, is this intended?
def clean(dataset: Dict[str, pd.DataFrame], dataset_n: Dict[str, pd.DataFrame]):
    # (1.1.1) Cleaning
    # (1.1.1.1) Clean up '----' in Hungarian entries
    dataset['hun.txt'] = dataset['hun.txt'][dataset['hun.txt']['V3'] != '----']
    # (1.1.1.2) Delete space in front of ' N;SG;NDEF' in Tajik entries
    dataset['tgk.txt']['V3'].replace('^ ', '', inplace=True, regex=True)
    # (1.1.1.3) Replace 'ADJ/GEN' with 'ADJ;GEN' in Armenian entries
    dataset['xcl.txt']['V3'].replace('ADJ/GEN', 'ADJ;GEN', inplace=True)
    # (1.1.1.4) Replace 'AJD' with 'ADJ' in Armenian entries
    dataset['xcl.txt']['V3'].replace('AJD', 'ADJ', inplace=True)
    # (1.1.1.5) Replace 'PCTP' with 'PTCP' in Slovenian entries
    dataset['slv.txt']['V3'].replace('PCTP', 'PTCP', inplace=True)

    # (3.1.2.1.1) Fixing Adyghe
    # why do we use .n for this code segment in the original code?
    dataset_n['ady.txt']['V3'].replace('N;ERG;PL;DEF;DEF', 'N;INS;PL;DEF', inplace=True)
    dataset_n['ady.txt']['V3'].replace('N;ERG;PL;DEF;NDEF', 'N;INS;PL;NDEF', inplace=True)
    dataset_n['ady.txt']['V3'].replace('N;ERG;SG;DEF;DEF', 'N;INS;SG;DEF', inplace=True)
    dataset_n['ady.txt']['V3'].replace('N;ERG;SG;DEF;NDEF', 'N;INS;SG;NDEF', inplace=True)

    # (3.1.4.2) 'ces.txt'
    dataset_n['ces.txt'].loc[dataset_n['ces.txt']['V3'].str.contains(';ANIM;'), 'V1'] = dataset_n['ces.txt']['V1'] + '-ANIM'
    dataset_n['ces.txt'].loc[dataset_n['ces.txt']['V3'].str.contains(';INAN;'), 'V1'] = dataset_n['ces.txt']['V1'] + '-INAN'
    dataset_n['ces.txt']['V3'].replace(';ANIM;', ';', inplace=True)
    dataset_n['ces.txt']['V3'].replace(';INAN;', ';', inplace=True)

    # (3.1.4.5) 'rus.txt'
    temp_anim = dataset_n['rus.txt'][dataset_n['rus.txt']['V3'] in ['N;ACC;ANIM;SG', 'N;ACC;ANIM;PL']]
    temp_anim = dataset_n['rus.txt'][dataset_n['rus.txt']['V1'] in temp_anim['V1'].unique()]
    temp_inan = dataset_n['rus.txt'][dataset_n['rus.txt']['V3'] in ['N;ACC;INAN;SG', 'N;ACC;INAN;PL']]
    temp_inan = dataset_n['rus.txt'][dataset_n['rus.txt']['V1'] in temp_inan['V1'].unique()]
    temp_other = dataset_n['rus.txt'][dataset_n['rus.txt']['V1'] not in temp_inan['V1'].unique()]

    temp_anim['V1'] = temp_anim['V1'] + '-ANIM'
    temp_anim = temp_anim[not temp_anim['V3'].str.contains(';INAN;')]
    temp_anim['V3'].replace(';ANIM;', ';', inplace=True)

    temp_inan['V1'] = temp_inan['V1'] + '-INAN'
    temp_inan = temp_inan[not temp_inan['V3'].str.contains(';ANIM;')]
    temp_inan['V3'].replace(';INAN;', ';', inplace=True)

    dataset_n['rus.txt'] = pd.concat([temp_anim, temp_inan, temp_other])
    dataset_n['rus.txt'].sort_values(by='V1', inplace=True)
