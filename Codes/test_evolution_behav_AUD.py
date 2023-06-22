# -*- coding: utf-8 -*-
"""
Created on Sat May 27 21:26:35 2023

@author: Pauline
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os
from statannot import add_stat_annotation
from openpyxl import Workbook
from path import perso_path_string
plt.rcParams["figure.figsize"] = (5,5)
perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)

Test_evol_PATH = P_folder_path + "Analysis/Test_evolution/Comportments/"

## RENAME VERSION ## + outliers
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
comportment_list = ["BDI", "Total_OCDS", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]


datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)



#%%
#PATIENTS T1 - PATIENTS T2 comportements comparison
comportment_list = ["BDI", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
fig = plt.figure(figsize=(8,3),constrained_layout = True)
value = 151
for c in comportment_list :
        print(c)
        df = datas_p[["T1_" + c, "T2_" + c]].copy().dropna(axis= 0)
        df["T1"] = datas_p["T1_" + c]
        df["T2"] = datas_p["T2_" + c]
        
        ttest = stats.ttest_rel(df["T1"].dropna() , df["T2"].dropna() )
        t_score, p_val = ttest
        print(ttest)
        
        if ( p_val < 0.05): 
            color_pal = ["indianred", "cadetblue"]
            color_mean = "white"
            #add_stat_annotation(ax, data=df, test='t-test_ind', text_format='star', order = ["Patients", "Controls"], loc='inside', verbose=2)
        else :
            color_pal = ["pink", "powderblue"]
            color_mean = "darkslategrey"
        
        mean_T1 = np.mean(df["T1"])
        mean_T2 = np.mean(df["T2"])
        
        plt.subplot(value)
        
        y= list(df["T1"]) + list(df["T2"])
        x = ["T1"]*len(list(df["T1"])) + ["T2"]*len(list(df["T2"]))
        
        sns.boxplot(y=list(df["T1"]) + list(df["T2"]),
                       x=["T1"]*len(list(df["T1"])) + ["T2"]*len(list(df["T2"])),
                       palette = color_pal, showmeans=True,meanprops={'marker':"o","markerfacecolor" : "dimgrey", "markeredgecolor" : "dimgrey", "markersize" : 5})
        #sns.violinplot(x=x, y=y,inner = "point", palette = color_pal ).set(title = c[:9])
        #sns.boxplot([abs_chang_p,abs_chang_c], width = 0.1)
        #plt.scatter(0,mean_T1, s = 700, marker ="_", c = color_mean)
        #plt.scatter(1,mean_T2, s = 700, marker ="_", c = color_mean)
        #sns.violinplot(y=y,x=x,palette = color, showmeans=True,meanprops={'marker':"_",'markeredgecolor':color_mean,'markersize':"40"})
        #sns.boxplot(df, palette = ["indianred", "cadetblue"])
        plt.title(c[:9])
        #plt.savefig(pat_cont_comparison_PATH + "Comportment/Pat_T1_T2_comparison_" + c+ ".png")
        #plt.show()   
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=True) # labels along the bottom edge are off
        value = value + 1

    
fig.suptitle("T1 - T2 comparison in AUDs", size = 15)
plt.savefig(Test_evol_PATH + "Pat_T1_T2_comparison.png")
plt.show()