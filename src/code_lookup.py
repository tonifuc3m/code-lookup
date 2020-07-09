#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:26:47 2020

@author: antonio
"""


from Levenshtein import distance as levenshtein_distance


def assign_code(_string, df_codes_info):
    '''
    Find in a dataframe the text span closer to a string. Returns the code
    associated with it.
    
    Parameters
    ----------
    df_codes_info: pandas dataframe
        Code information. It has at least the columns 'span' and 'code'
    string: str
        String I am comparing
           
    Returns
    -------
    code: str
        Assigned code
    
    '''
    
    idx = df_codes_info['span'].apply(lambda x: levenshtein_distance(_string, x)).idxmin()
    
    return str(df_codes_info.loc[idx, 'code'])
    

def code_lookup(df_annots, df_codes_info):
    '''
    Assigns codes to dataframe with annotations based on a second dataset
    with codes informations
    
    Parameters
    ----------
    df_codes_info: pandas dataframe
        Code information. It has at least the columns 'span' and 'code'
    df_annots: pandas dataframe
        Annotations. It has all columns needed to reconstruct the annotations
        files: 'filename', 'mark', 'label', 'offset1', 'offset2', 'span', 'code'
           
    Returns
    -------
    df_annots: pandas dataframe
        Annotations. It has all columns needed to reconstruct the annotations
        files: 'filename', 'mark', 'label', 'offset1', 'offset2', 'span', 'code'
    '''
    
    for idx, _ in df_annots.iterrows():
        _string = df_annots.loc[idx, 'span']
        code = assign_code(_string, df_codes_info)
        df_annots.loc[idx, 'code'] = code
        
    return df_annots