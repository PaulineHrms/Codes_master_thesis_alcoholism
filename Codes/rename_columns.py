# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:36:30 2023

@author: Pauline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os
from path import perso_path_string
plt.rcParams["figure.figsize"] = (5,5)
perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)
#Test_evol_PATH = P_folder_path + "Analysis/Patients/Test_evolution/"




region_list = ["cc_tract", "cc_tract_genu", "cc_tract_ant_midbody", "cc_tract_post_midbody", "cc_tract_isthmus", "cc_tract_splenium", "uf.left", "uf.right", "uf"]
new_region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]

models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "diamond_fractions_csf" , "diamond_fractions_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
time = ["E1", "E2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]

rename_compportment_controls = {"BDI" : "T1_BDI", 
                                "OCDS_total": "T1_Total_OCDS",
                                "OCDS_obsessions" : "T1_OCDS_Obsessions" ,
                                "OCDS_compulsions" : "T1_OCDS_Compulsions",
                                "STAI" : "T1_STAI",
                                "MFI" : "T1_MFI"}

rename_compportment_patients = {"T1_OCDS_MODIFIE_Total": "T1_Total_OCDS",
                                "T2_OCDS_MODIFIE_Total": "T2_Total_OCDS",
                                "T3_OCDS_MODIFIE_Total": "T3_Total_OCDS",
                                "T1_STAI_YA" : "T1_STAI",
                                "T2_STAI_YA" : "T2_STAI",
                                "T3_STAI_YA" : "T3_STAI"}

rename_microstructure = {}

for model in models:
    for metric in metric_list[model]:
        for i in range(len(region_list)):
            if metric == "diamond_fractions_csf":
                rename_microstructure["wMean_" + metric + "_" + model + "_E1_" + region_list[i]] = "wMean_frac_csf_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["wMean_" + metric + "_" + model + "_E2_" + region_list[i]] = "wMean_frac_csf_" + model + "_T2_" + new_region_list[i]
                
                rename_microstructure["Std_" + metric + "_" + model + "_E1_" + region_list[i]] = "Std_frac_csf_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["Std_" + metric + "_" + model + "_E2_" + region_list[i]] = "Std_frac_csf_" + model + "_T2_" + new_region_list[i]
            
            elif metric == "diamond_fractions_ftot":
                rename_microstructure["wMean_" + metric + "_" + model + "_E1_" + region_list[i]] = "wMean_frac_ftot_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["wMean_" + metric + "_" + model + "_E2_" + region_list[i]] = "wMean_frac_ftot_" + model + "_T2_" + new_region_list[i]
                
                rename_microstructure["Std_" + metric + "_" + model + "_E1_" + region_list[i]] = "Std_frac_ftot_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["Std_" + metric + "_" + model + "_E2_" + region_list[i]] = "Std_frac_ftot_" + model + "_T2_" + new_region_list[i]
                
            else : 
                rename_microstructure["wMean_" + metric + "_" + model + "_E1_" + region_list[i]] = "wMean_" + metric + "_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["wMean_" + metric + "_" + model + "_E2_" + region_list[i]] = "wMean_" + metric + "_" + model + "_T2_" + new_region_list[i]
                
                rename_microstructure["Std_" + metric + "_" + model + "_E1_" + region_list[i]] = "Std_" + metric + "_" + model + "_T1_" + new_region_list[i]
                rename_microstructure["Std_" + metric + "_" + model + "_E2_" + region_list[i]] = "Std_" + metric + "_" + model + "_T2_" + new_region_list[i]
                
for col in  Stream_list:
    for i in range(len(region_list)):
        rename_microstructure[col + "_E1_" + region_list[i]] = col + "_T1_" + new_region_list[i]
        rename_microstructure[col + "_E2_" + region_list[i]] = col + "_T2_" + new_region_list[i]
        

#%%

datas_c = pd.read_excel(excel_path + "data_alcoholic_controlswhiteNoise.xlsx",index_col=0 )

rename1_data_c = datas_c.rename(columns=rename_compportment_controls).copy()

new_datas_c = rename1_data_c.rename(columns=rename_microstructure).copy()

new_datas_c.to_excel(excel_path+"data_alcoholic_controls_rename.xlsx")

#%%

datas_c = pd.read_excel(excel_path + "data_alcoholic_patientswhiteNoise.xlsx",index_col=0 )

rename1_data_c = datas_c.rename(columns=rename_compportment_patients).copy()

new_datas_c = rename1_data_c.rename(columns=rename_microstructure).copy()

new_datas_c.to_excel(excel_path+"data_alcoholic_patients_rename.xlsx")