# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:53:50 2023

@author: Pauline
"""

#Creation of the DataFrame

import pandas as pd
import numpy as np
from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=True)


names = ["Numéro", "N_adm", "Nom", "Prénom", "DN", "T1_BDI", "T1_OCDS_MODIFIE_Total",	"T1_OCDS_Obsessions",	"T1_OCDS_Compulsions",	"T1_STAI_YA", "T1_STAI_YB",	"T1_MFI", "T2_Bearni",	"T2_BDI",	"T2_OCDS_MODIFIE_Total",	"T2_OCDS_Obsessions",	"T2_OCDS_Compulsions",	"T2_STAI_YA", "T2_STAI_YB",	"T2_MFI",	"T2_Mini_big_five",	"SHP",	"NSHP",	"SMP",	"NSMP",	"SLP",	"NSLP",	"Wellbeing",	"Selfconfidence",	"Emotion",	"Sociability",	"Motivation",	"Adaptation",	"Total_TEIQUE", "T2_PTSD"]
data = pd.read_excel(excel_path + "General_data_alcoholic.xlsx", usecols = names)

data["Numéro"] = data["Numéro"].map("sub{}".format)
data["Numéro"] = data["Numéro"].replace(["sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8","sub9"], ["sub01","sub02","sub03", "sub04","sub05","sub06","sub07","sub08","sub09"])


data.to_excel(excel_path + "data_alcoholic_patients.xlsx")


#data.head(2)