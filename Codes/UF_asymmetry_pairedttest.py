# -*- coding: utf-8 -*-
"""
Created on Fri May 26 21:16:20 2023

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
UF_asym_PATH = analysis_path + "UF_asymmetry_PAIRED/"

## RENAME VERSION + outliers ##
region_list = ["CC", "CC_genu", "CC_ant_midbody", "CC_post_midbody", "CC_isthmus", "CC_splenium", "UF_left", "UF_right", "UF"]
models = ["dti","diamond", "mf", "noddi"]
metric_list = {"dti" : ["FA", "MD", "AD", "RD"],"diamond" : ["wFA", "wMD", "wAD", "wRD" , "frac_csf" , "frac_ftot"],"mf" : ["fvf_tot", "frac_csf", "frac_ftot", "wfvf"],"noddi" : ["fiso", "fintra", "fextra", "odi"]}
time = ["T1", "T2"]
Stream_list = ["nb_stream", "mean_streamDensity", "std_streamDensity"]
hemisphere = ["right", "left"]
groupes_list = ["patients","controls"]

colors = ["indianred","lightcoral","cadetblue","lightblue"]


datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)
datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)




for model in models:
    if not os.path.exists(UF_asym_PATH + model + "/" ): 
        os.mkdir(UF_asym_PATH + model + "/")
    for metric in metric_list[model]:
        if not os.path.exists(UF_asym_PATH  + model + "/" + metric): 
            os.mkdir(UF_asym_PATH  + model + "/" + metric)
                
if not os.path.exists(UF_asym_PATH + "UF_asymmetry_P.xlsx")  :
    wb = Workbook()
    wb.save(UF_asym_PATH + "UF_asymmetry_P.xlsx")         
       
#%%
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)
datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)

  
#Normaliser la densité de fibres par la densité total dans tout le cerveau
dic_density = np.load(excel_path + "dictionnary_tracto_density_controls.npy",allow_pickle='TRUE').item()

subjects_list_p = list(datas_p["Numéro"])

for sub in subjects_list_p:
    for t in time:   
        subject = sub + "_E" + t[1]
        if subject in list(dic_density.keys()):
            for region in ["UF_left", "UF_right", "UF"]:
                mean_density = datas_p[datas_p["Numéro"] == sub]["mean_streamDensity_" + t+ "_" + region]
                
                tot_density = dic_density[subject]["tot_density"]
                datas_p.loc[datas_p["Numéro"] == sub,["mean_streamDensity_" + t+ "_" + region]] = mean_density/tot_density

subjects_list_c = list(datas_c["Numéro"])

for sub in subjects_list_c:
    for t in time:   
        subject = sub + "_E" + t[1]
        if subject in list(dic_density.keys()):
            for region in ["UF_left", "UF_right", "UF"]:
                mean_density = datas_c[datas_c["Numéro"] == sub]["mean_streamDensity_" + t+ "_" + region]
                
                tot_density = dic_density[subject]["tot_density"]

                datas_c.loc[datas_c["Numéro"] == sub,["mean_streamDensity_" + t+ "_" + region]] = mean_density/tot_density  


excel = {"T1":pd.DataFrame(), "T2":pd.DataFrame()}
excel["T1"].index = ["p","c", "p&c"]
excel["T2"].index = ["p","c", "p&c"]

for t in time:
    print(t)
    for col in Stream_list :
        
        UF_p = datas_p[[col + "_" + t + "_UF_left",col + "_" + t + "_UF_right"]].copy().dropna(axis=0)
        UF_c = datas_c[[col + "_" + t + "_UF_left",col + "_" + t + "_UF_right"]].copy().dropna(axis=0)

        UFl_p = pd.DataFrame(UF_p[col + "_" + t + "_UF_left"])
        UFr_p = pd.DataFrame(UF_p[col + "_" + t + "_UF_right"])
        
        UFl_c = pd.DataFrame(UF_c[col + "_" + t + "_UF_left"])
        UFr_c = pd.DataFrame(UF_c[col + "_" + t + "_UF_right"])
        
        df_left = pd.concat([UFl_p,UFl_c,UFr_p,UFr_c],ignore_index=True)
        df_right = pd.concat([UFr_p,UFr_c])
        df = {"right" : {"controls": UFr_c,"patients" : UFr_p},"left" : {"controls": UFl_c,"patients" : UFl_p}}

        data = pd.DataFrame()
        col_names = {}
        names = {}
        for groupe in groupes_list:
            for h in hemisphere:
                col_names[col+ "_" + t + "_UF_"+h+"_"+groupe] = groupe + "_" + h[0].upper()
                data[col+ "_" + t + "_UF_"+h+"_"+groupe] = df[h][groupe][col+ "_" + t + "_UF_"+h]
                names[groupe + "_" + h[0].upper()] = "f"
        
        names_plot= {'patients_R': 'AUD right', 'patients_L': 'AUD left', 'controls_R': 'CS right', 'controls_L': 'CS left'}
        data = data.rename(columns=col_names)
        data_plot = data.rename(columns= names_plot)
        sns.set(font_scale = 1.3)
        sns.boxplot(data=data_plot, palette = colors )
        plt.title(col + " at " + t, fontsize = 16)
        plt.savefig(UF_asym_PATH+"UF_asymmetry_P_"+ col +"_"+t)
        plt.show()    
        
        pR = np.asarray(data["patients_R"].dropna())
        pL = np.asarray(data["patients_L"].dropna())
        cR = np.asarray(data["controls_R"].dropna())
        cL = np.asarray(data["controls_L"].dropna())
        
        t_test = stats.ttest_rel(pR, pL,alternative='two-sided')
        excel[t].loc[excel[t].index == "p",[col]] = t_test[1]
        
        t_test = stats.ttest_rel(cR, cL,alternative='two-sided')
        excel[t].loc[excel[t].index == "c",[col]] = t_test[1]
      
        L = np.concatenate((pL, cL))
        R = np.concatenate((pR, cR))
        t_test = stats.ttest_rel(L, R,alternative='two-sided')
        excel[t].loc[excel[t].index == "p&c",[col]] = t_test[1]
        
        
        print(col)
        print("Mean pR ", np.mean(pR))
        print("Mean pL ", np.mean(pL))
        print("% = ", np.mean(pR/pL))
        print("Mean cR ", np.mean(cR))
        print("Mean cL ", np.mean(cL))
        print("% = ", np.mean(cR/cL))
        print("Mean R ", np.mean(R))
        print("Mean L ", np.mean(L))
        print("% = ", np.mean(R/L))

with pd.ExcelWriter(UF_asym_PATH + "UF_asymmetry_P.xlsx",
                engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
    excel['T1'].to_excel(writer, sheet_name="Density_T1")
    excel['T2'].to_excel(writer, sheet_name="Density_T2")
#%%       
if False:       
        lists = [pR, pL, cR, cL]
        names = ["pR", "pL", "cR", "cL"]
        
        L = np.concatenate((pL, cL))
        R = np.concatenate((pR, cR))
        t_test = stats.ttest_ind(L, R, equal_var = False)
        excel.loc[excel.index == "stat",["L/R"]] = t_test[0]
        excel.loc[excel.index == "p_val",["L/R"]] = t_test[1]
        #print("L","R",t_test)
        
        p = np.concatenate((pL, pR))
        c = np.concatenate((cL, cR))
        t_test = stats.ttest_ind(p, c, equal_var = False)
        excel.loc[excel.index == "stat",["p/c"]] = t_test[0]
        excel.loc[excel.index == "p_val",["p/c"]] = t_test[1]
        #print("p","c",t_test)
        
        for i in range(4):
            for j in range(i):
                if not (np.array_equal(lists[i], lists[j])):
                    t_test = stats.ttest_ind(lists[i], lists[j], equal_var = False)
                    excel.loc[excel.index == names[i],[names[j]]] = t_test[1]
                    excel.loc[excel.index == names[j],[names[i]]] = t_test[1]
                    #print(i,j,t_test)
       
        with pd.ExcelWriter(UF_asym_PATH + "UF_asymmetry.xlsx",
                        engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
            excel.to_excel(writer, sheet_name=col + "_" +t)



#%%

#models = ["dti"]          
datas_p = pd.read_excel(excel_path + "data_alcoholic_patients_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)
datas_c = pd.read_excel(excel_path + "data_alcoholic_controls_rename_without_outliers.xlsx",index_col=0).replace(["/", "perdu", "incomplet"], np.nan)


excel_metrics = {"T1":pd.DataFrame(), "T2":pd.DataFrame(), "DIFF" : pd.DataFrame() }
excel_metrics["T1"].index = ["p","c", "p&c"]
excel_metrics["T2"].index = ["p","c", "p&c"]
excel_metrics["DIFF"].index = ["p","c", "p&c"]
for model in models:
    for metric in metric_list[model]:
        a = """UF_p = datas_p[["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left","wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"]].copy().dropna(axis=0)
        UF_c = datas_c[["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left","wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"]].copy().dropna(axis=0)

        UFl_p = pd.DataFrame(UF_p[col + "_" + t + "_UF_left"])
        UFr_p = pd.DataFrame(UF_p[col + "_" + t + "_UF_right"])
        
        UFl_c = pd.DataFrame(UF_c[col + "_" + t + "_UF_left"])
        UFr_c = pd.DataFrame(UF_c[col + "_" + t + "_UF_right"])
        
        UFl_p = (datas_p[["wMean_"+ metric + "_"+ model+"_T1_UF_left","wMean_"+ metric + "_"+ model+"_T2_UF_left"]]).copy()
        UFr_p = (datas_p[["wMean_"+ metric + "_"+ model+"_T1_UF_right","wMean_"+ metric + "_"+ model+"_T2_UF_right"]]).copy()
        
        UFl_c = (datas_c[["wMean_"+ metric + "_"+ model+"_T1_UF_left","wMean_"+ metric + "_"+ model+"_T2_UF_left"]]).copy()
        UFr_c = (datas_c[["wMean_"+ metric + "_"+ model+"_T1_UF_right","wMean_"+ metric + "_"+ model+"_T2_UF_right"]]).copy()"""
        
        for t in time:
            UF_p = datas_p[["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left","wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"]].copy().dropna(axis=0)
            UF_c = datas_c[["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left","wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"]].copy().dropna(axis=0)


            Pl = pd.DataFrame(UF_p["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left"])
            Pr = pd.DataFrame(UF_p["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"])
            
            Cl = pd.DataFrame(UF_c["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_left"])
            Cr = pd.DataFrame(UF_c["wMean_"+ metric + "_"+ model+ "_" + t + "_UF_right"])
            
            df_left = pd.concat([Pl,Cl],ignore_index=True)
            df_right = pd.concat([Pr,Cr])
            df = {"right" : {"controls": Cr,"patients" : Pr},"left" : {"controls": Cl,"patients" : Pl}}
    
            data = pd.DataFrame()
            col_names = {}
            for groupe in groupes_list:
                for h in hemisphere:
                    #print(groupe,h)
                    col_names["wMean_"+ metric + "_"+ model+"_"+t+"_UF_"+h+"_"+groupe] = groupe + "_" + h[0].upper()
                    data["wMean_"+ metric + "_"+ model+"_"+t+"_UF_"+h+"_"+groupe] = df[h][groupe]#["wMean_"+ metric + "_"+ model+"_"+t+"_UF_"+h]
                    
            data = data.rename(columns=col_names)
            sns.boxplot(data=data, palette = colors )
            plt.title(metric + " ("+ model+") at "+t)
            plt.savefig(UF_asym_PATH + model + "/"+metric+"/UF_asym_P_comparison_"+ model + "_" + metric +"_"+t+".png")
            plt.show()    
            
            pR = np.asarray(data["patients_R"].dropna())
            pL = np.asarray(data["patients_L"].dropna())
            cR = np.asarray(data["controls_R"].dropna())
            cL = np.asarray(data["controls_L"].dropna())
            

            t_test = stats.ttest_rel(pR, pL)
            excel_metrics[t].loc[excel_metrics[t].index == "p",[model + "_" + metric +"_"+t]] = t_test[1]
            
            t_test = stats.ttest_rel(cR, cL)
            excel_metrics[t].loc[excel_metrics[t].index == "c",[model + "_" + metric +"_"+t]] = t_test[1]
          
            L = np.concatenate((pL, cL))
            R = np.concatenate((pR, cR))
            t_test = stats.ttest_rel(L, R)
            excel_metrics[t].loc[excel_metrics[t].index == "p&c",[model + "_" + metric +"_"+t]] = t_test[1]

        

        UF_p = (datas_p[["wMean_"+ metric + "_"+ model+"_T1_UF_left","wMean_"+ metric + "_"+ model+"_T2_UF_left",
                          "wMean_"+ metric + "_"+ model+"_T1_UF_right","wMean_"+ metric + "_"+ model+"_T2_UF_right"]]).copy().dropna(axis=0)
        
        UF_c = (datas_c[["wMean_"+ metric + "_"+ model+"_T1_UF_left","wMean_"+ metric + "_"+ model+"_T2_UF_left",
                          "wMean_"+ metric + "_"+ model+"_T1_UF_right","wMean_"+ metric + "_"+ model+"_T2_UF_right"]]).copy().dropna(axis=0)


        
        UFl_p["patients_L"] = UF_p["wMean_"+ metric + "_"+ model+"_T1_UF_left"] - UF_p["wMean_"+ metric + "_"+ model+"_T2_UF_left"]
        UFr_p["patients_R"] = UF_p["wMean_"+ metric + "_"+ model+"_T1_UF_right"] - UF_p["wMean_"+ metric + "_"+ model+"_T2_UF_right"]
        UFl_c["controls_L"] = UF_c["wMean_"+ metric + "_"+ model+"_T1_UF_left"] - UF_c["wMean_"+ metric + "_"+ model+"_T2_UF_left"]
        UFr_c["controls_R"] = UF_c["wMean_"+ metric + "_"+ model+"_T1_UF_right"] - UF_c["wMean_"+ metric + "_"+ model+"_T2_UF_right"]
        
        
        df_left = pd.concat([UFl_p["patients_L"],UFl_c["controls_L"]],ignore_index=True)
        df_right = pd.concat([UFr_p["patients_R"],UFr_c["controls_R"]])
        df = {"right" : {"controls": UFr_c["controls_R"],"patients" : UFr_p["patients_R"]},"left" : {"controls": UFl_c["controls_L"],"patients" : UFl_p["patients_L"]}}
        
        data = pd.DataFrame([UFl_p["patients_L"],UFr_p["patients_R"],UFl_c["controls_L"],UFr_c["controls_R"]]).T
        
        sns.boxplot(data=data, palette = colors )
        plt.title("Evolution of " + metric + " (" + model+ ")")
        plt.savefig(UF_asym_PATH + model + "/"+metric+"/Hemisphere_comparison_"+ model + "_" + metric +"_DIFF.png")
        plt.show()    
        
        pR = np.asarray(data["patients_R"].dropna())
        pL = np.asarray(data["patients_L"].dropna())
        cR = np.asarray(data["controls_R"].dropna())
        cL = np.asarray(data["controls_L"].dropna())

    
        t_test = stats.ttest_rel(pR, pL)
        excel_metrics["DIFF"].loc[excel_metrics["DIFF"].index == "p",[model + "_" + metric +"_"+t]] = t_test[1]
        
        t_test = stats.ttest_rel(cR, cL)
        excel_metrics["DIFF"].loc[excel_metrics["DIFF"].index == "c",[model + "_" + metric +"_"+t]] = t_test[1]
      
        L = np.concatenate((pL, cL))
        R = np.concatenate((pR, cR))
        t_test = stats.ttest_rel(L, R)
        excel_metrics["DIFF"].loc[excel_metrics["DIFF"].index == "p&c",[model + "_" + metric +"_"+t]] = t_test[1]
    
 
    

    
with pd.ExcelWriter(UF_asym_PATH + "UF_asymmetry_P.xlsx",
                engine='openpyxl',mode='a', if_sheet_exists = 'replace') as writer:  
    excel_metrics['T1'].to_excel(writer, sheet_name="T1")
    excel_metrics['T2'].to_excel(writer, sheet_name="T2")
    excel_metrics['DIFF'].to_excel(writer, sheet_name="Diff")
   
