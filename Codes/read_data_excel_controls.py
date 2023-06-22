# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 15:44:37 2023

@author: Pauline
"""


#Creation of the DataFrame

import pandas as pd
import numpy as np
from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)


names = ["Numéro IRM cluster", "Nom", "Prénom", "DN", "BDI", "OCDS_total",	"OCDS_obsessions",	"OCDS_compulsions",	"STAI", "MFI", "Bearni",	"Mini big 5",	"S_SHP",	"S_NSHP",	"S_SMP",	"S_NSMP",	"S_SLP",	"S_NSLP"]
data = pd.read_excel(excel_path + "Controles.xlsx", usecols = names)


data = data.rename(columns={"Numéro IRM cluster": "Numéro"})

data["Numéro"] = data["Numéro"].map("sub{}".format)


data.to_excel(excel_path + "data_alcoholic_controls.xlsx")


#data.head(2)