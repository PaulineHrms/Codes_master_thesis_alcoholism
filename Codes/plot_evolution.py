# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:52:24 2023

@author: Pauline
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
Test_evol_PATH = P_folder_path + "Analysis/Test_evolution/"


## RENAME VERSION ## + OUTLIERS
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
comportment_list = ["BDI", "Total_OCDS", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]

datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)



for cible in ["All"]:
    for model in models:
        if not os.path.exists(Test_evol_PATH + "/"+ cible + "/" + model + "/" ): 
            os.mkdir(Test_evol_PATH + "/" + cible + "/" + model + "/")
        for metric in metric_list[model]:
            if not os.path.exists(Test_evol_PATH + "/" + cible + "/" + model + "/" + metric): 
                os.mkdir(Test_evol_PATH + "/" + cible + "/" + model + "/" + metric)

            
#%%


for model in models:
    for metric in metric_list[model]:
        for region in region_list:
            
            data_p = (datas_p[["wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region]]).copy().dropna(axis = 0)
            data_c = (datas_c[["wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region]]).copy().dropna(axis = 0)
            
            #for controls
            data_T1_c = np.asarray(data_c["wMean_"+ metric + "_"+ model+"_T1_"+region])
            data_T2_c = np.asarray(data_c["wMean_"+ metric + "_"+ model+"_T2_"+region])
            
            
            #for patients
            data_T1_p = np.asarray(data_p["wMean_"+ metric + "_"+ model+"_T1_"+region])
            data_T2_p = np.asarray(data_p["wMean_"+ metric + "_"+ model+"_T2_"+region])
            
          
            #figures
            fig, ax = plt.subplots()            
            labels = ['T1', 'T2', "T1", "T2"]
            
            y=list(data_T1_p) + list(data_T2_p) + list(data_T1_c) + list(data_T2_c)
            x=["T1 \n AUD"]*len(list(data_T1_p)) + ["T2 \n AUD"]*len(list(data_T2_p)) + ["T1 \n CS"]*len(list(data_T1_c)) + ["T2 \n CS"]*len(list(data_T2_c))
            sns.violinplot(y=y,x=x,showmeans=True,showmedians=False, palette = ["darkseagreen","cadetblue", "indianred", "sandybrown"] )
            
            #sns.violinplot([data_T1_p, data_T2_p],showmeans=True,showmedians=False, palette = ["darkseagreen","cadetblue"] )
            ax.yaxis.grid(True)
            #ax.set_xticks([y for y in range(4)], labels=['T1', 'T2',"T1", "T2"])
            plt.title("Evolution " + model + " " + metric + " in " + region + "\n AUD vs CS")
            
            x = [0,1]
            for i in range(len(data_T1_p)):
                y = [data_T1_p[i], data_T2_p[i]]
                plt.plot(x,y, color="lightsteelblue", alpha= 0.5)
                
            x = [2,3]
            for i in range(len(data_T1_c)):
                y = [data_T1_c[i], data_T2_c[i]]
                plt.plot(x,y, color="lightsteelblue", alpha= 0.5)
            
            
            plt.savefig(Test_evol_PATH+ "/All/" + model + "/" + metric + "/Evolution " + model + "-" + metric + "-" + region + ".png")
            plt.show()
            
             
#%%

      


for model in models:
    for metric in metric_list[model]:
            #df = pd.DataFrame(region_list, columns=(["Region"]))
            fig = plt.figure(figsize=(14,4),constrained_layout = True)
            value = 191
            for region in region_list:
                
                df = pd.DataFrame()
                
                data_p = (datas_p[["wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region]]).copy().dropna(axis = 0)
                data_c = (datas_c[["wMean_"+ metric + "_"+ model+"_T1_"+region, "wMean_"+ metric + "_"+ model+"_T2_"+region]]).copy().dropna(axis = 0)
                
                #for patients
                data_T1_p = np.asarray(data_p["wMean_"+ metric + "_"+ model+"_T1_"+region])
                data_T2_p = np.asarray(data_p["wMean_"+ metric + "_"+ model+"_T2_"+region])
                abs_chang_p = abs((data_T2_p - data_T1_p)/data_T1_p)
                mean_p = np.mean(abs_chang_p)
                df["AUD"] = pd.DataFrame(abs_chang_p)
                
                #for controls
                data_T1_c = np.asarray(data_c["wMean_"+ metric + "_"+ model+"_T1_"+region])
                data_T2_c = np.asarray(data_c["wMean_"+ metric + "_"+ model+"_T2_"+region])
                abs_chang_c = abs((data_T2_c - data_T1_c)/data_T1_c)
                mean_c = np.mean(abs_chang_c)
                df["CS"] = pd.DataFrame(abs_chang_c)
                
                
                
                if ( mean_p > mean_c): 
                    color_pal = ["indianred", "cadetblue"]
                    color_mean = "white"
                    #add_stat_annotation(ax, data=df, test='t-test_ind', text_format='star', order = ["Patients", "Controls"], loc='inside', verbose=2)
                else :
                    color_pal = ["pink", "powderblue"]
                    color_mean = "darkslategrey"
    
                y=list(abs_chang_p)  + list(abs_chang_c)
                x=["AUD"]*len(list(abs_chang_p)) +  ["CS"]*len(list(abs_chang_c)) 
                            
    
                plt.subplot(value)
                sns.violinplot(x=x, y=y,inner = "point", palette = color_pal ).set(title = region[:11])
                #sns.boxplot([abs_chang_p,abs_chang_c], width = 0.1)
                plt.scatter(0,mean_p, s = 700, marker ="_", c = color_mean)
                plt.scatter(1,mean_c, s = 700, marker ="_", c = color_mean)

                plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=True) # labels along the bottom edge are off
                
                value = value + 1
    
                
            fig.suptitle('Percentage of changes ' + metric + " (" + model + ")", size = 20)
            plt.savefig(Test_evol_PATH + "/Evolution_comp_"+metric + "_" + model + ".png")
            plt.show()


