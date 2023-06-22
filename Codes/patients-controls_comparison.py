# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:07:08 2023

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

pat_cont_comparison_PATH = P_folder_path + "Analysis/P-C_comparison/"

## RENAME VERSION ## + outliers
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
comportment_list = ["BDI", "Total_OCDS", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]

datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0 ).replace(["/", "perdu", "incomplet"], np.nan)

df_pval = {"T1" : pd.DataFrame(region_list, columns=(["Region"])), "T2" : pd.DataFrame(region_list, columns=(["Region"]))}
df_diff =  {"T1" : pd.DataFrame(region_list, columns=(["Region"])), "T2" : pd.DataFrame(region_list, columns=(["Region"]))}


for model in models:
    if not os.path.exists(pat_cont_comparison_PATH + model + "/" ): 
        os.mkdir(pat_cont_comparison_PATH + model + "/")
    for metric in metric_list[model]:
        if not os.path.exists(pat_cont_comparison_PATH + model + "/" + metric): 
            os.mkdir(pat_cont_comparison_PATH + model + "/" + metric)



if not os.path.exists(pat_cont_comparison_PATH + "Comportment/"): 
    os.mkdir(pat_cont_comparison_PATH + "Comportment/")

if not os.path.exists(pat_cont_comparison_PATH + "Patients-Controls_comparison.xlsx")  :
    wb = Workbook()
    wb.save(pat_cont_comparison_PATH + "Patients-Controls_comparison.xlsx")

#%%

#models = ["dti"]
#region_list = ["CC", "UF"]

for model in models:
    for metric in metric_list[model]:
        for t in time:
            
            for region in region_list:
                df = pd.DataFrame()
                
                df["Patients"] = datas_p["wMean_" + metric + "_" + model + "_" + t + "_" + region].dropna()
                df["Controls"] = datas_c["wMean_" + metric + "_" + model + "_" + t + "_" + region].dropna()
                
                ttest = stats.ttest_ind(df["Patients"].dropna() , df["Controls"].dropna() , equal_var = False)
                t_score, p_val = ttest
                print(ttest)
                df_pval[t].loc[df_pval[t]["Region"] == region,[metric+"_"+model]] = p_val
                
                mean_c = np.mean(df["Controls"])
                mean_p = np.mean(df["Patients"])
                DIFF = mean_c - mean_p
                print(mean_c, mean_p, DIFF)
                df_diff[t].loc[df_diff[t]["Region"] == region,[metric+"_"+model]] = DIFF
                
                
                sns.boxplot(y=list(df["Patients"]) + list(df["Controls"]),
                               x=["Patients"]*len(list(df["Patients"])) + ["Controls"]*len(list(df["Controls"])),
                               palette = ["indianred", "cadetblue"], showmeans=True,meanprops={'marker':"o","markerfacecolor" : "dimgrey", "markeredgecolor" : "dimgrey", "markersize" : 5}).set(title = region[:11])
                plt.title(metric + " " + model + " in "  + region + " at " + t)
                plt.savefig(pat_cont_comparison_PATH + model + "/" + metric+"/Pat-Contr_DIFF_"+metric + "_" + model + "_" + t + "_" + region+ ".png")
                plt.show()
                
                
                
                

with pd.ExcelWriter(pat_cont_comparison_PATH + "Patients-Controls_comparison.xlsx",
                    engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
    df_pval["T1"].to_excel(writer, sheet_name="T1")  
    df_pval["T2"].to_excel(writer, sheet_name="T2")
    df_diff["T1"].to_excel(writer, sheet_name="Diff_T1")  
    df_diff["T2"].to_excel(writer, sheet_name="Diff_T2")
              
                
#%%

df_pval = pd.DataFrame(comportment_list, columns=(["Behavioural metrics"]))
df_diff = pd.DataFrame(comportment_list, columns=(["Behavioural metrics"]))

for c in comportment_list :
    for t in time:
        df = pd.DataFrame()
        df["Patients"] = datas_p[t + "_" + c]
        df["Controls"] = datas_c["T1_" + c]
        
        ttest = stats.ttest_ind(df["Patients"].dropna() , df["Controls"].dropna() , equal_var = False)
        t_score, p_val = ttest
        print(ttest)
        df_pval.loc[df_pval["Behavioural metrics"] == c,[t]] = p_val
        
        
        mean_c = np.mean(df["Controls"])
        mean_p = np.mean(df["Patients"])
        DIFF = mean_c - mean_p
        print(mean_c, mean_p, DIFF)
        df_diff.loc[df_diff["Behavioural metrics"] == c,[t]] = DIFF
        
        
        sns.boxplot(y=list(df["Patients"]) + list(df["Controls"]),
                       x=["Patients"]*len(list(df["Patients"])) + ["Controls"]*len(list(df["Controls"])),
                       palette = ["indianred", "cadetblue"], showmeans=True,meanprops={'marker':"o","markerfacecolor" : "dimgrey", "markeredgecolor" : "dimgrey", "markersize" : 5})
        #sns.boxplot(df, palette = ["indianred", "cadetblue"])
        plt.title(c + " at " + t +" (for patients)")
        plt.savefig(pat_cont_comparison_PATH + "Comportment/Pat-Contr_DIFF_"+ t + "_" + c+ ".png")
        
        plt.show()
        
with pd.ExcelWriter(pat_cont_comparison_PATH + "Patients-Controls_comparison.xlsx",
                    engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
    df_pval.to_excel(writer, sheet_name="Comportment")
    df_diff.to_excel(writer, sheet_name="Diff_Comportment")
    
    
    
#%%




for model in models:
    for metric in metric_list[model]:
        for t in time:
            #df = pd.DataFrame(region_list, columns=(["Region"]))
            fig = plt.figure(figsize=(12,3),constrained_layout = True)
            value = 191
            for region in region_list:
                
                
                df = pd.DataFrame()
                df["AUD"] = datas_p["wMean_" + metric + "_" + model + "_" + t + "_" + region].dropna()
                df["CS"] = datas_c["wMean_" + metric + "_" + model + "_" + t + "_" + region].dropna()
                #print(value,region, df.columns)
                
                
                ttest = stats.ttest_ind(df["AUD"].dropna() , df["CS"].dropna(), equal_var = False)
                if (ttest[1] <0.05): 
                    color = ["indianred", "cadetblue"]
                    mean_color = 'dimgrey'
                    #add_stat_annotation(ax, data=df, test='t-test_ind', text_format='star', order = ["Patients", "Controls"], loc='inside', verbose=2)
                else :
                    color = ["pink", "powderblue"]
                    mean_color = 'grey'
                    
                plt.subplot(value)
                #sns.boxplot(df, palette = color).set(title = region[:11])
                sns.boxplot(y=list(df["AUD"]) + list(df["CS"]),
                               x=["AUD"]*len(list(df["AUD"])) + ["CS"]*len(list(df["CS"])),
                                   palette = color, showmeans=True,meanprops={'marker':"o","markerfacecolor" : mean_color,
                                            "markeredgecolor" : "dimgrey", "markersize" : 5}).set(title = region[:11])
                
                plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
                plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=True) # labels along the bottom edge are off
                value = value + 1
    
                
            fig.suptitle( "Patient-control comparison for " + metric + " (" + model + ") at " + t, size = 12)
            plt.savefig(pat_cont_comparison_PATH + "/Pat-Contr_DIFF_"+metric + "_" + model + "_" + t + ".png")
            plt.show()
                

             
#%%

comportment_list = ["BDI", "OCDS_Obsessions", "OCDS_Compulsions", "STAI","MFI"]

for c in comportment_list :
    for t in time:
        df = pd.DataFrame()
        df["Patients"] = datas_p[t + "_" + c]
        df["Controls"] = datas_c["T1_" + c]
        
        ttest = stats.ttest_ind(df["Patients"].dropna() , df["Controls"].dropna() , equal_var = False)
        t_score, p_val = ttest
        print(ttest)
        df_pval.loc[df_pval["Behavioural metrics"] == c,[t]] = p_val

        

    

for t in time:
    #df = pd.DataFrame(region_list, columns=(["Region"]))
    fig = plt.figure(figsize=(8,3),constrained_layout = True)
    value = 151
    for c in comportment_list :
        
        
        df = pd.DataFrame()
        df["AUD"] = datas_p[t + "_" + c]
        df["CS"] = datas_c["T1_" + c]
       
        #plt.savefig(PATH_savefig + "\Boxplot_" + c + "_evolution.png")
        #Max = np.max(np.max(df))
        ttest = stats.ttest_ind(df["AUD"].dropna() , df["CS"].dropna(), equal_var = False)
        if (ttest[1] <0.05): 
            color = ["indianred", "cadetblue"]
            mean_color = 'dimgrey'
            #add_stat_annotation(ax, data=df, test='t-test_ind', text_format='star', order = ["Patients", "Controls"], loc='inside', verbose=2)
        else :
            color = ["pink", "powderblue"]
            mean_color = 'grey'

        plt.subplot(value)
        sns.boxplot(y=list(df["AUD"]) + list(df["CS"]),
                       x=["AUD"]*len(list(df["AUD"])) + ["CS"]*len(list(df["CS"])),
                       palette = color, showmeans=True,meanprops={'marker':"o","markerfacecolor" : mean_color,
                                    "markeredgecolor" : "dimgrey", "markersize" : 5}).set(title =(c[:9] + "\n p-val = "+ str(format(ttest[1], ".1e")) ))
        

        #plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=True) # labels along the bottom edge are off
        value = value + 1

        
    #fig.suptitle('Boxplot of ' + model + " " + metric + " at " + t)
    plt.savefig(pat_cont_comparison_PATH + "/Pat-Contr_DIFF_behav_" + t + ".png")
    plt.show()

