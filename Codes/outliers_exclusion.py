# -*- coding: utf-8 -*-
"""
Created on Tue May 16 21:18:29 2023

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

## RENAME VERSION ##
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
comportment_list = ["BDI", "Total_OCDS", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]


outliers = {"Patients": 
                {"microstructure" : 
                      {"T1" :
                          {"all" : ["sub01","sub03", "sub06", "sub07", "sub08", "sub10", "sub17", "sub21", "sub25", "sub27", "sub34", "sub36", "sub40", "sub47", "sub48", "sub49"],
                          "region" : 
                               {"CC" : [ "sub31"], 
                                "CC_genu" : [ "sub31"],
                                "CC_ant_midbody" : ["sub11", "sub31"],
                                "CC_post_midbody" : ["sub22", "sub31"],
                                "CC_isthmus" : ["sub22", "sub31", "sub50"],
                                "CC_splenium" : [ "sub31"],
                                "UF_left" : ["sub22", "sub24", "sub43"],
                                "UF_right" : [ "sub24"],
                                "UF" : [ "sub24"]},
                          "model" : 
                               {"dti" : [],
                                "diamond" : [],
                                "mf" : [],
                                "noddi" : []}},
                       "T2" : 
                           {"all" : ["sub01","sub10", "sub11", "sub16", "sub17", "sub23", "sub29", "sub34", "sub36", "sub38", "sub42", "sub44", "sub47", "sub49", "sub52"],
                           "region" : 
                                {"CC" : ["sub48"], 
                                 "CC_genu" : ["sub48"],
                                 "CC_ant_midbody" : ["sub48"],
                                 "CC_post_midbody" : ["sub48"],
                                 "CC_isthmus" : ["sub48"],
                                 "CC_splenium" : ["sub48"],
                                 "UF_left" : [ "sub24", "sub43"],
                                 "UF_right" : ["sub14", "sub24"],
                                 "UF" : ["sub24"]},
                           "model" : 
                                {"dti" : [],
                                 "diamond" : [],
                                 "mf" : [],
                                 "noddi" : []}}},
                          
                "comportment" : {
                    "T1" : {
                           'BDI': [], 
                           'Total_OCDS': [], 
                           'OCDS_Obsessions': [], 
                           'OCDS_Compulsions': [], 
                           'STAI': [], 
                           'MFI': []},
                    "T2": {
                           'BDI': ["sub02", "sub15", "sub16", "sub17", "sub19", "sub23", "sub48"], 
                           'Total_OCDS': ["sub15", "sub16", "sub19", "sub48"], 
                           'OCDS_Obsessions': ["sub15", "sub16", "sub19", "sub48"], 
                           'OCDS_Compulsions': ["sub15", "sub16", "sub19"], 
                           'STAI': ["sub02","sub15", "sub16", "sub17", "sub19"], 
                           'MFI': ["sub15", "sub16", "sub19"]}}},
        "Controls" :
                {"microstructure" : 
                      {"T1" :
                          {"all" : [],
                          "region" : 
                               {"CC" : ["sub61", "sub71"], 
                                "CC_genu" : ["sub61", "sub71"],
                                "CC_ant_midbody" : ["sub61", "sub71"],
                                "CC_post_midbody" : ["sub61", "sub71"],
                                "CC_isthmus" : ["sub61", "sub71"],
                                "CC_splenium" : ["sub61", "sub71"],
                                "UF_left" : ["sub69"],
                                "UF_right" : [],
                                "UF" : []},
                           "model" : 
                               {"dti" : [],
                                "diamond" : [],
                                "mf" : [],
                                "noddi" : []}},
                       "T2" : 
                           {"all" : ["sub56"],
                           "region" : 
                                {"CC" : ["sub61", "sub71"], 
                                 "CC_genu" : ["sub61", "sub71"],
                                 "CC_ant_midbody" : ["sub61", "sub71"],
                                 "CC_post_midbody" : ["sub61", "sub71"],
                                 "CC_isthmus" : ["sub61", "sub71"],
                                 "CC_splenium" : ["sub61", "sub71"],
                                 "UF_left" : [],
                                 "UF_right" : [],
                                 "UF" : []},
                        "model" : 
                                {"dti" : [],
                                 "diamond" : [],
                                 "mf" : [],
                                 "noddi" : []}}},
                          
                "comportment" : 
                     {'BDI': ["sub57"], 
                      'Total_OCDS': ["sub57", "sub62", "sub69", "sub70"], 
                      'OCDS_Obsessions': ["sub57", "sub62", "sub69"], 
                      'OCDS_Compulsions': ["sub57", "sub62", "sub69", "sub70"], 
                      'STAI': ["sub54", "sub57"], 
                      'MFI': ["sub57"]}}}
    
#%%


datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)

#Patients microstructure
for t in time:
    for r in region_list:
        subjects_list = outliers["Patients"]["microstructure"][t]["all"] + outliers["Patients"]["microstructure"][t]["region"][r]
        print(t+"_"+r, subjects_list)
        for sub in subjects_list :
            for model in models:
                for m in metric_list[model]:
                    datas_p.loc[datas_p["Numéro"] == sub,["wMean_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
                    datas_p.loc[datas_p["Numéro"] == sub,["Std_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
#Patients comportment
for t in time:
    for c in comportment_list:
        subjects_list = outliers["Patients"]["comportment"][t][c]
        print(t , c, subjects_list)
        for sub in subjects_list:
            datas_p.loc[datas_p["Numéro"] == sub,[t+"_"+c]] = np.nan

datas_p.to_excel(excel_path+"data_alcoholic_patients_rename_without_outliers.xlsx")

#%%

#"Controls" microstructure
for t in time:
    for r in region_list:
        subjects_list = outliers["Controls"]["microstructure"][t]["all"] + outliers["Controls"]["microstructure"][t]["region"][r]
        print(t+"_"+r, subjects_list)
        for sub in subjects_list :
            for model in models:
                for m in metric_list[model]:
                    datas_c.loc[datas_c["Numéro"] == sub,["wMean_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
                    datas_c.loc[datas_c["Numéro"] == sub,["Std_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
                    
model = "mf"
sub = "sub67"
for t in time:
    for m in metric_list[model]:
        for r in region_list:
            datas_c.loc[datas_c["Numéro"] == sub,["wMean_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
            datas_c.loc[datas_c["Numéro"] == sub,["Std_"+m+"_"+model+"_"+t+"_"+r]] = np.nan
                       
#"Controls" comportment

for c in comportment_list:
    subjects_list = outliers["Controls"]["comportment"][c]
    print( c, subjects_list)
    for sub in subjects_list:
        datas_c.loc[datas_c["Numéro"] == sub,["T1_"+c]] = np.nan
        
datas_c.to_excel(excel_path+"data_alcoholic_controls_rename_without_outliers.xlsx")
