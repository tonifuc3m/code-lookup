#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:14:24 2020

@author: antonio
"""

import os
from utils.parse import parse_ann, parse_tsv
from utils.general_utils import argparser, write_ann, copy_txt_files
from code_lookup import code_lookup

if __name__ == '__main__':
    annot_path, codes_path, outpath = argparser()
    
    '''
    annot_path = '/home/antonio/Documents/Work/BSC/Projects/Tasks/Cantemist/baseline/char-lookup/pred'
    codes_path = '/home/antonio/Documents/Work/BSC/Projects/Tasks/Cantemist/data/oncology/gloria/last-version-data-20200625/all-1-7'
    outpath = '/home/antonio/Documents/Work/BSC/Projects/Tasks/Cantemist/baseline/char-lookup/pred-norm'
    '''
    labels_to_ignore = ['_REJ_MORFOLOGIA_NEOPLASIA', '_SUG_MORFOLOGIA_NEOPLASIA',
                        'MORFOLOGIA_PREDICTED']
    ## Parse codes
    if os.path.isfile(codes_path):
        codes_info = parse_tsv(codes_path)
    else:
        codes_info = parse_ann(codes_path, labels_to_ignore = labels_to_ignore, 
                               with_notes=True)
    codes_info = codes_info.drop_duplicates(subset=['span', 'code'])[['span', 'code']]
    
    
    ## Parse annotations
    annots = parse_ann(annot_path)
    annots = annots[['filename', 'mark', 'label', 'offset1', 'offset2','span']]
    annots['code'] = 'UNK'
    
    ## Add codes to annotations  
    annots_with_code = code_lookup(annots, codes_info)
    
    ## Write annotation files in output
    filenames = set(annots_with_code['filename'].tolist())
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for f in filenames:
        write_ann(f, annots_with_code, outpath)
        
    ## Copy txt files
    copy_txt_files(annot_path, outpath)
