#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:14:53 2020

@author: antonio
"""
import argparse
import os
from shutil import copyfile


def argparser():
    '''
    DESCRIPTION: Parse command line arguments
    '''
    
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("-d", "--annot_path", required = True, dest = "annot_path", 
                        help = "path to directory with annotations")
    parser.add_argument("-c", "--codes_path", required = True, dest = "codes_path", 
                        help = "path directory or file with codes information")
    parser.add_argument("-o", "--outpath", required =  True, dest="outpath", 
                        help = "path to output directory")
    args = parser.parse_args()
    
    return args.annot_path, args.codes_path, args.outpath


def write_ann(filename, df_annots, outpath):
    '''
    Write ANN files from dataframe
        
    Parameters
    ----------
    filename: str.
        File name
    df_annots: pandas dataframe
        Dataframe with annotations. It has all columns needed to reconstruct 
        the annotations files: 'filename', 'mark', 'label', 'offset1', 
        'offset2', 'span', 'code'
    outpath: str. 
        Target directory.
    
    
    '''
    df_this = df_annots[df_annots['filename']==filename]
    f = open(os.path.join(outpath, filename), 'w')
    for idx,_ in df_this.iterrows():
        mark = df_this.loc[idx,'mark']
        label = df_this.loc[idx, 'label']
        off0 = df_this.loc[idx,'offset1']
        off1 = df_this.loc[idx,'offset2']
        span = df_this.loc[idx,'span']
        code = df_this.loc[idx,'code']
        f.write(mark + '\t' + label + ' ' + off0 + ' ' + off1 + '\t' + span + '\n')
        f.write('#' + mark[1:] + '\t' + 'AnnotatorNotes' + ' ' + mark + '\t' + code + '\n')
        
    f.close()
    
    
                
def copy_txt_files(datapath, outpath):
    '''
    Copy .txt files from one directory to another. It keeps folder structure.
        
    Parameters
    ----------
    datapath: str.
        Source directory.
    outpath: str. 
        Target directory.
    '''
    for root, dirs, files in os.walk(datapath):
        for fname in files:
            if fname.endswith('txt') == False:
                continue
            copyfile(os.path.join(root,fname), 
                     os.path.join(outpath, root[len(datapath):], fname))
            
    
    
