# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:21:51 2023

@author: Pauline
"""

from TIME.utils import tract_to_ROI, get_streamline_density
import nibabel as nib
import numpy as np
from dipy.io.streamline import load_tractogram
import pandas as pd
import sys, os

from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)




def ROI_tract(subject, subjects_path, P_folder_path):

    region_list = ["25_250000_1_D_uf"]#["cc_tract", "cc_tract_genu", "cc_tract_ant_midbody", "cc_tract_post_midbody", "cc_tract_isthmus", "cc_tract_splenium", "uf.left", "uf.right", "uf"]
    
    sub = subject[:5]
    E = subject[6:]
    
    PATH_study = subjects_path + subject 
    PATH_diamond = PATH_study +"/dMRI/microstructure/diamond/" 
    PATH_wmql = P_folder_path +"Data/wmql/" + subject + "/"
    PATH_roi = P_folder_path + "Data/ROI/" + subject + "/"
    
    img = nib.load(PATH_diamond + subject + "_wFA.nii.gz")
    
    
    
    for region in region_list:
        print(region)
        
        if os.path.exists(PATH_wmql  + subject + "_" + region +".trk"):
            #Creation of the ROI for the tractography of each region
            roi = tract_to_ROI(PATH_wmql  + subject + "_" + region +".trk")
            
            if not os.path.exists(PATH_roi):
                os.makedirs(PATH_roi)
            out = nib.Nifti1Image(roi,img.affine)
            out.to_filename(PATH_roi + subject +"_roi_" + region + ".nii.gz")
            
           
                    

#Patients_list = ["sub41_E1", "sub27_E1", "sub32_E1", "sub09_E1", "sub45_E1", "sub48_E1", "sub21_E1", "sub05_E1", "sub15_E1", "sub11_E1", "sub46_E1", "sub31_E1", "sub16_E1", "sub26_E1", "sub50_E1", "sub22_E1", "sub47_E1", "sub44_E1", "sub02_E1", "sub53_E1", "sub18_E1", "sub01_E1", "sub34_E1", "sub35_E1", "sub51_E1", "sub23_E1", "sub04_E1", "sub38_E1", "sub19_E1", "sub28_E1", "sub24_E1", "sub33_E1", "sub37_E1", "sub29_E1", "sub14_E1", "sub13_E1", "sub36_E1", "sub12_E1", "sub43_E1", "sub40_E1", "sub45_E3", "sub20_E1", "sub39_E1", "sub17_E1", "sub52_E1", "sub42_E1", "sub08_E1", "sub10_E1", "sub30_E1", "sub32_E2", "sub29_E2", "sub53_E2", "sub31_E2", "sub39_E2", "sub07_E2", "sub45_E2", "sub13_E2", "sub24_E2", "sub42_E2", "sub11_E2", "sub25_E2", "sub21_E2", "sub08_E2", "sub01_E2", "sub09_E2", "sub50_E2", "sub22_E2", "sub34_E2", "sub30_E2", "sub37_E2", "sub12_E2", "sub20_E2", "sub17_E2", "sub14_E2", "sub04_E2", "sub05_E2", "sub06_E2", "sub33_E2", "sub35_E2", "sub43_E2", "sub27_E2", "sub28_E2", "sub19_E2", "sub15_E2", "sub26_E2", "sub02_E2", "sub40_E2", "sub18_E2", "sub52_E2", "sub51_E2", "sub36_E2", "sub48_E2", "sub46_E2", "sub03_E2", "sub41_E2", "sub27_E3", "sub34_E3", "sub09_E3", "sub02_E3", "sub30_E3", "sub17_E3", "sub36_E3", "sub22_E3", "sub20_E3", "sub39_E3", "sub03_E3"]

Patients_list = ["sub51_E1"]#["sub09_E1", "sub09_E2", "sub19_E1", "sub19_E2", "sub54_E2", "sub55_E1"]
for sub in Patients_list : 
    ROI_tract(sub, subjects_path, P_folder_path)





