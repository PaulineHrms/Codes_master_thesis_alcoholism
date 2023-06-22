# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:14:51 2023

@author: Pauline (inspired from Corpus_callosum_division.py by Manon Dausort)

Update of the FreeSurfer parcellation to divide the corpus callosum in 5 regions according to
specific arithmetic ration.  /!\ Only for CONTROLS data
"""

import numpy as np
import nibabel as nib
import os, sys
from scipy.ndimage import affine_transform

from path import perso_path_string


def CC_division(patient, division_fracs, Freesurfer_path, P_folder_path):
    wmparc_path =  Freesurfer_path + patient +"/mri/wmparc.mgz"
    wmparc_load = nib.load(wmparc_path)
    wmparc = wmparc_load.get_fdata().astype('int32')
    
    wmparc_new = wmparc.copy()
    
    cc_mask = np.where(250<wmparc_new, wmparc_new, 0)
    cc_mask = np.where(cc_mask<256, cc_mask, 0)
    
    ind = np.where(cc_mask>0)
    
    coord_min = min(ind[2])
    coord_max = max(ind[2])
    len_CC = coord_max - coord_min
    
    
    
    coord2_splenium = round(coord_min)
    coord1_splenium = round(coord_min + len_CC * division_fracs[0])
    coord2_isthmus = round(coord1_splenium)
    coord1_isthmus = round(coord_min + len_CC * division_fracs[1])
    coord2_posterior = round(coord1_isthmus)
    coord1_posterior = round(coord_min + len_CC * division_fracs[2])
    coord2_anterior = round(coord1_posterior)
    coord1_anterior = round(coord_min + len_CC * division_fracs[3])
    coord2_genu = round(coord_min + len_CC * division_fracs[3])
    coord1_genu = round(coord_max)
    
    
    for i in range(wmparc_new.shape[0]):
        wmparc_new[i,:,coord2_genu:coord1_genu] = int(5255)
    
        wmparc_new[i,:,coord2_anterior:coord1_anterior] = int(5254)
    
        wmparc_new[i,:,coord2_posterior:coord1_posterior] = int(5253)
    
        wmparc_new[i,:,coord2_isthmus:coord1_isthmus] = int(5252)
    
        wmparc_new[i,:,coord2_splenium:coord1_splenium] = int(5251)
        
    new_wmparc = np.where(cc_mask > 1,wmparc_new, wmparc)
    
    
    write_path = P_folder_path+"Data/wmql/"+patient+"/"
    if not os.path.exists(write_path):
      os.makedirs(write_path) 
      
    out = nib.Nifti1Image(new_wmparc, affine=wmparc_load.affine, header=wmparc_load.header)
    out.to_filename(write_path + "new_wmparc_"+patient+".nii.gz")


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=True)
folder_path = patients_path

Freesurfer_path = "/CECI/proj/pilab/PermeableAccess/alcooliques_As2Z4vF8GNv/Camille_folder/Recon-all-controles/"

patient = sys.argv[1]

division_fracs = [1/4, 1/3, 1/2, 5/6]

CC_division(patient, division_fracs, Freesurfer_path, P_folder_path)
