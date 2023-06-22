# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 09:39:29 2023

@author: Pauline

Compute and plot the correlation between evolution (absolute difference) of each comportement scores and
evolution (absolute difference) of each metrics and each regions. 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os
from openpyxl import Workbook
from path import perso_path_string

plt.rcParams["figure.figsize"] = (5,5)
perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)
Corr_evol_PATH = P_folder_path + "Analysis/Correlation_evolution/"

#Definition variables
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
comportment_list = ["BDI", "Total_OCDS", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]

#Download datas
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)


#Create folders
for model in models:
    if not os.path.exists(Corr_evol_PATH + model + "/" ): 
        os.mkdir(Corr_evol_PATH + model + "/")
    for metric in metric_list[model]:
        if not os.path.exists(Corr_evol_PATH + model + "/"+metric ): 
            os.mkdir(Corr_evol_PATH + model + "/"+metric)

df_sign = {
       'BDI': [], 
       'Total_OCDS': [], 
       'OCDS_Obsessions': [], 
       'OCDS_Compulsions': [], 
       'STAI': [], 
       'MFI': []}

#%%

for c in comportment_list : 

    if not os.path.exists(Corr_evol_PATH + "Correlations_diff_patients.xlsx")  :
        wb = Workbook()
        wb.save(Corr_evol_PATH + "Correlations_diff_patients.xlsx")
    
    data_corr = pd.DataFrame(region_list, columns = ["regions" ])
    
    if not os.path.exists(Corr_evol_PATH + "p_val_correlations_diff_patients.xlsx")  :
        wb = Workbook()
        wb.save(Corr_evol_PATH + "p_val_correlations_diff_patients.xlsx")
        
    data_p_val = pd.DataFrame(region_list, columns = ["regions" ])
     
     
    for model in models:
        for metric in metric_list[model]:
             
            max_x,max_y,min_x,min_y = 0,0,0,0
            dic = {}
            for region in region_list:
                data_complet = (datas_p[["Numéro","wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region, "T1_"+c, "T2_"+c]]).copy()
                
                data = data_complet.dropna(axis = 0)
  
                dic["data_"+region] = data 
  
                data_m1 = data["wMean_"+ metric + "_"+ model+"_T1_"+region]
                data_m2 = data["wMean_"+ metric + "_"+ model+"_T2_"+region]
                data_c1 = data["T1_"+c]
                data_c2 = data["T2_"+c]
                
                data["diff_"+model + "_"+ metric+"_"+region] = data_m2 - data_m1
                data["diff_"+c] = data_c2 - data_c1
                
                max_x = max(max_x, max(data["diff_"+model + "_"+ metric+"_"+region]))
                min_x = min(min_x, min(data["diff_"+model + "_"+ metric+"_"+region]))
                
            max_x, min_x = max_x*1.1, min_x*1.1    
            max_y = (max(data["diff_"+c]))*1.1
            min_y = (min(data["diff_"+c]))*1.1
            
            for region in region_list:
                data = dic["data_"+region]
                
                m = "diff_"+model + "_"+ metric+"_"+region
                comp = "diff_"+c
                
                
                pearson = stats.pearsonr(data[m], data[comp])
                data_corr.loc[data_corr["regions"] == region,[model + "_"+ metric]] = pearson[0]
                data_p_val.loc[data_corr["regions"] == region,[model + "_"+ metric]] = pearson[1]
                
                if (pearson[1] < 0.05): 
                    df_sign[c].append([model, metric, region])
                
                if (np.max(data["diff_"+model + "_"+ metric+"_"+region]) < 0.01) :
                    plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
                plt.xlim([min_x, max_x])
                plt.ylim([min_y, max_y])
                sns.regplot(x=m,y=comp, data = data, label = "Subjects",
                            line_kws=({'label' :"Regression", "color": "cadetblue"}), 
                            scatter_kws=({'color' : "indianred"}), truncate = False)
                
                text1 = "Pearson coef = "+str(pearson[0])[:5]
                text2 = "p_val = "+str(pearson[1])[:5]
                plt.text(1.1* max_x, 0.9 *max_y,text1 + "\n" + text2)
                
                plt.plot([0,0],[min_y,max_y], color = 'k',alpha = 0.2)
                plt.plot([min_x,max_x],[0,0], color = 'k',alpha=0.2)
                plt.xlabel("Difference of " + metric + " (" + model + ") in " + region)
                plt.ylabel("Difference of " + c + " scores")
                plt.grid(False)
                
                plt.title( metric+ " (" + model + ") in the " + region[:11])
                plt.legend()
                plt.savefig(Corr_evol_PATH+model + "/"+metric+"/Correlation_diff_"+c+"_"+model + "_"+ metric+"_" + region +".png" )
                plt.show()
            
            with pd.ExcelWriter(Corr_evol_PATH+"Correlations_diff_patients.xlsx",
                            engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
                data_corr.to_excel(writer, sheet_name=c)
                
            with pd.ExcelWriter(Corr_evol_PATH+"p_val_correlations_diff_patients.xlsx",
                            engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
                data_p_val.to_excel(writer, sheet_name=c)
    

#%%


def graph(c, mmr, val, size):
    fig = plt.figure(figsize=(size[0],size[1]),constrained_layout = True)
    value = val
    
    for i in range(len(mmr)):
        
        model, metric, region = mmr[i]


        data_complet = (datas_p[["Numéro","wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region, "T1_"+c, "T2_"+c]]).copy()
        
        data = data_complet.dropna(axis = 0)

        dic["data_"+region] = data 
        
        #print(data.shape, model + "_"+ metric+"_"+region)    
        data_m1 = data["wMean_"+ metric + "_"+ model+"_T1_"+region]
        data_m2 = data["wMean_"+ metric + "_"+ model+"_T2_"+region]
        data_c1 = data["T1_"+c]
        data_c2 = data["T2_"+c]
        
        data["diff_"+model + "_"+ metric+"_"+region] = data_m2 - data_m1
        data["diff_"+c] = data_c2 - data_c1
        
        max_x = np.max(data["diff_"+model + "_"+ metric+"_"+region])
        min_x = np.min(data["diff_"+model + "_"+ metric+"_"+region])
            
        max_x, min_x = max_x*1.1, min_x*1.1    
        max_y = (max(data["diff_"+c]))*1.1
        min_y = (min(data["diff_"+c]))*1.1
             
        m = "diff_"+model + "_"+ metric+"_"+region
        comp = "diff_"+c
         
        pearson = stats.pearsonr(data[m], data[comp])

        plt.subplot(value)
        if (np.max(data["diff_"+model + "_"+ metric+"_"+region]) < 0.01) :
            plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
        plt.xlim([min_x, max_x])
        plt.ylim([min_y, max_y])
        a, b = np.polyfit(data[m], data[comp], 1)
        sns.regplot(x=m,y=comp, data = data, label = "Subjects",
                    line_kws=({'label' :"Regression", "color": "cadetblue"}), 
                    scatter_kws=({'color' : "indianred"}), truncate = False)
        plt.plot([0,0],[min_y,max_y], color = 'k',alpha = 0.2)
        plt.plot([min_x,max_x],[0,0], color = 'k',alpha=0.2)
        
        if value == val:
            plt.ylabel("Difference of " + c[:9] , size = 14)
        else : 
            plt.ylabel(" ")
        plt.xlabel("Difference of " + metric , size=14)
        if region == "CC_ant_midbody":
            region = "CC_ant_m-b."
        if region == "CC_post_midbody":
            region = "CC_post_m-b."
        plt.title(metric+" ("+ model + ") in " + region[:11] + "\nPearson = " + str(pearson[1])[:4] + ", pval = " + str(pearson[1])[:5], size=15)
        
        plt.legend(framealpha = 0.25, edgecolor = "k", fontsize = 10)
        value = value +1
    
    #plt.show()
#%% 

df_sign = {'BDI': [['diamond', 'wFA', 'CC_isthmus'],
                  ['diamond', 'wRD', 'CC_post_midbody']],
             'OCDS_Obsessions': [['dti', 'FA', 'CC'],
                  ['dti', 'RD', 'CC_genu'],
                  ['diamond', 'wRD', 'CC'],
                  ['mf', 'fvf_tot', 'CC'],
                  ['mf', 'fvf_tot', 'CC_genu'],
                  ['mf', 'wfvf', 'CC'],
                  ['mf', 'wfvf', 'CC_genu'],
                  ['mf', 'wfvf', 'CC_ant_midbody'],
                  ['noddi', 'fintra', 'CC_genu'],
                  ['noddi', 'fintra', 'UF_right']],
             'OCDS_Compulsions': [['diamond', 'wRD', 'CC'],
                  ['diamond', 'wRD', 'CC_splenium'],
                  ['mf', 'fvf_tot', 'CC'],
                  ['mf', 'wfvf', 'CC'],
                  ['mf', 'wfvf', 'CC_splenium']],
             'STAI': [['diamond', 'wFA', 'CC_splenium'],
                  ['diamond', 'frac_csf', 'CC_splenium'],
                  ['diamond', 'frac_ftot', 'CC_splenium'],
                  ['noddi', 'fintra', 'UF_left']],
             'MFI': [['diamond', 'wMD', 'CC_isthmus'],
                  ['diamond', 'wAD', 'CC_isthmus'],
                  ['noddi', 'fextra', 'CC_isthmus']]}
   
graph("BDI", df_sign["BDI"], 121, [8,3])
plt.savefig(Corr_evol_PATH+"BDI.png")
plt.show()

graph("MFI", df_sign["MFI"], 131, [12,3])
plt.savefig(Corr_evol_PATH+"MFI.png")
plt.show()

graph("STAI", df_sign["STAI"], 141, [16,3])
plt.savefig(Corr_evol_PATH+"STAI.png")
plt.show()


OCDS_Compul = [ ['diamond', 'wRD', 'CC'], ['mf', 'fvf_tot', 'CC'],  ['mf', 'wfvf', 'CC_splenium']]

OCDS_Comp_annexe = [['diamond', 'wRD', 'CC_splenium'],['mf', 'wfvf', 'CC']]

graph("OCDS_Compulsions", OCDS_Compul, 131, [12,3])
plt.savefig(Corr_evol_PATH+"OCDS_Compul(1).png")
plt.show()
graph("OCDS_Compulsions", OCDS_Comp_annexe, 121, [8,3])
plt.savefig(Corr_evol_PATH+"OCDS_Compul(annexe).png")
plt.show()



OCDS_Obs = [['dti', 'FA', 'CC'],  ['dti', 'RD', 'CC_genu'],  ['diamond', 'wRD', 'CC'], ['mf', 'fvf_tot', 'CC_genu'],
            ['mf', 'wfvf', 'CC_ant_midbody'],  ['noddi', 'fintra', 'UF_right']]

OCDS_Obs_annexe= [['mf', 'fvf_tot', 'CC'],  ['mf', 'wfvf', 'CC'], ['mf', 'wfvf', 'CC_genu'],['noddi', 'fintra', 'CC_genu']]

graph("OCDS_Obsessions", OCDS_Obs[:3], 131, [12,3])
plt.savefig(Corr_evol_PATH+"OCDS_Obs(1).png")
plt.show()
graph("OCDS_Obsessions", OCDS_Obs[3:], 131, [12,3])
plt.savefig(Corr_evol_PATH+"OCDS_Obs(2).png")
plt.show()

graph("OCDS_Obsessions", OCDS_Obs_annexe[:2], 121, [8,3])
plt.savefig(Corr_evol_PATH+"OCDS_Obs(annexe1).png")
plt.show()

graph("OCDS_Obsessions", OCDS_Obs_annexe[2:], 121, [8,3])
plt.savefig(Corr_evol_PATH+"OCDS_Obs(annexe2).png")
plt.show()




