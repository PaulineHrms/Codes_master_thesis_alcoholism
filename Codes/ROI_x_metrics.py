# -*- coding: utf-8 -*-
"""
Created on Thu May 11 11:37:48 2023

@author: Pauline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import nibabel as nib
import os
from openpyxl import Workbook
from path import perso_path_string
plt.rcParams["figure.figsize"] = (5,5)
perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)
Corr_evol_PATH = P_folder_path + "Analysis/Patients/Correlation_evolution/diff/"

datas = pd.read_excel(excel_path + "data_alcoholic_patients.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)


region_list = ["cc_tract", "cc_tract_genu", "cc_tract_ant_midbody", "cc_tract_post_midbody", "cc_tract_isthmus", "cc_tract_splenium", "uf.left", "uf.right", "uf"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "diamond_fractions_csf" , "diamond_fractions_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
time = ["E1", "E2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]
comportement =  ["BDI", "OCDS_MODIFIE_Total","OCDS_Obsessions","OCDS_Compulsions","STAI_YA","MFI"]

outliers = {"BDI" : ["sub02"],
           "OCDS_MODIFIE_Total" : ["sub21"],
           "OCDS_Obsessions" : ["sub21"],
           "OCDS_Compulsions" : [],
           "STAI_YA" : ["sub21","sub06"],
           "MFI" : ["sub25","sub34"]}

ROI_PATH = "C:/Users/Pauline/Desktop/Memoire/Data/Pauline_folder/Data/StreamDensity/sub65_E1/sub65_E1_streamdensity_cc_tract.nii.gz"
FA_PATH = "C:/Users/Pauline/Desktop/Memoire/Data/alcoholic_study/subjects/sub65_E1/dMRI/microstructure/diamond/sub65_E1_wFA.nii.gz"
AD_PATH = "C:/Users/Pauline/Desktop/Memoire/Data/alcoholic_study/subjects/sub65_E1/dMRI/microstructure/diamond/sub65_E1_wAD.nii.gz"
RD_PATH = "C:/Users/Pauline/Desktop/Memoire/Data/alcoholic_study/subjects/sub65_E1/dMRI/microstructure/diamond/sub65_E1_wRD.nii.gz"

ROI_load = nib.load(ROI_PATH)
ROI = ROI_load.get_fdata()
print(ROI)
FA_load = nib.load(FA_PATH)
FA = np.nan_to_num(FA_load.get_fdata())
print(FA)
AD_load = nib.load(AD_PATH)
AD = np.nan_to_num(AD_load.get_fdata())
print(AD)
RD_load = nib.load(RD_PATH)
RD = np.nan_to_num(RD_load.get_fdata())
print(RD)


Combi = ROI*RD

write_path = "C:/Users/Pauline/Desktop/Memoire/Data/Pauline_folder/Data/T1_visualization/sub65_E1/cc_ROI_&_DMD_wRD.nii.gz" 
out = nib.Nifti1Image(Combi, affine=ROI_load.affine, header=ROI_load.header)
out.to_filename(write_path)


