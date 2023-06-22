# -*- coding: utf-8 -*-
"""
Created on Wed May 17 10:53:32 2023

@author: Pauline
"""


from TIME.utils import  get_streamline_density
import nibabel as nib
import numpy as np
from dipy.io.streamline import load_tractogram
import pandas as pd
import sys, os

from path import perso_path_string



perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)


def tracto_density(subject, subjects_path, P_folder_path):
    
    tracto_PATH = subjects_path + subject + "/dMRI/tractography/" + subject + "_tracto_25_250000_1.trk"

        
    #Calculation of the number of streamlines
    trk = load_tractogram(tracto_PATH, "same")
    trk.to_vox()
    trk.to_corner() 
    
    nb_stream = len(trk.streamlines._offsets)

    img_density = get_streamline_density(trk)
    total_density = np.sum(img_density)
    
    
    
    return nb_stream, total_density
    

    

subject = sys.argv[1] 
    
nb_stream, total_density = tracto_density(subject, subjects_path, P_folder_path)


df_density = np.load(excel_path + "dictionnary_tracto_density.npy",allow_pickle='TRUE').item()
df_density[subject]= {}
df_density[subject]["nb_stream"] = nb_stream
df_density[subject]["tot_density"] = total_density
np.save(excel_path + "dictionnary_tracto_density.npy", df_density) 


