# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 09:14:26 2022

@author: Fauston

Compute DIAMOND metric maps
"""

import numpy as np
import nibabel as nib
# import time
import sys
from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)

def get_FA_DIAMOND(subjects_path, patient_path):

    """
        Parameters
        ----------
        subjects_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
    
        Returns
        -------
        None. But creation of files containing the cFA, cMD, cAD and cRD for each patient. "c" stands for compartment.
    """
    
    tenseur_list = ["t0", "t1"]       
    
    for tenseur in tenseur_list:
        
        path = subjects_path + patient_path + "/dMRI/microstructure/dti/" + patient_path + "_FA.nii.gz"
        
        comp = subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_" + tenseur + ".nii.gz"
        comp = nib.load(comp).get_fdata()
       
        MD = np.zeros((comp.shape[0],comp.shape[1],comp.shape[2]))
        AD = np.zeros((comp.shape[0],comp.shape[1],comp.shape[2]))
        RD = np.zeros((comp.shape[0],comp.shape[1],comp.shape[2]))
        FA = np.zeros((comp.shape[0],comp.shape[1],comp.shape[2]))
        
        
        D = np.array([[np.squeeze(comp[:,:,:,:,0]), np.squeeze(comp[:,:,:,:,1]), np.squeeze(comp[:,:,:,:,3])],
                      [np.squeeze(comp[:,:,:,:,1]), np.squeeze(comp[:,:,:,:,2]), np.squeeze(comp[:,:,:,:,4])],
                      [np.squeeze(comp[:,:,:,:,3]), np.squeeze(comp[:,:,:,:,4]), np.squeeze(comp[:,:,:,:,5])]])
        

        for i in range(comp.shape[0]):
            for j in range(comp.shape[1]):
                for k in range(comp.shape[2]):
                    
                    valeurs_propres = np.array(np.linalg.eigvals(D[:,:,i,j,k]))
                    max_valeur = max(np.abs(valeurs_propres))
                    index_lambda = [l for l in range(len(valeurs_propres)) if abs(valeurs_propres[l])==max_valeur]
        
                    copy_valeurs_propres = np.copy(valeurs_propres)
                    copy_valeurs_propres = np.delete(copy_valeurs_propres, index_lambda[0])
                    copy_valeurs_propres = np.array(copy_valeurs_propres)
                    
                    MD[i,j,k] = (valeurs_propres[0] + valeurs_propres[1] + valeurs_propres[2])/3
                    AD[i,j,k] = valeurs_propres[index_lambda[0]]
                    RD[i,j,k] = (copy_valeurs_propres[0]+copy_valeurs_propres[1])/2
                    
                    if((valeurs_propres[0]**2 + valeurs_propres[1]**2 + valeurs_propres[2]**2) == 0):
                        FA[i,j,k] = 0
                    else:
                        FA[i,j,k] = np.sqrt(3/2)*np.sqrt(((valeurs_propres[0] - MD[i,j,k])**2 + (valeurs_propres[1] - MD[i,j,k])**2 + (valeurs_propres[2] - MD[i,j,k])**2)/(valeurs_propres[0]**2 + valeurs_propres[1]**2 + valeurs_propres[2]**2))
                    
        out = nib.Nifti1Image(MD, affine = nib.load(path).affine, header = nib.load(path).header)
        out.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_MD_DMD_" + tenseur + ".nii.gz")
        
        out1 = nib.Nifti1Image(AD, affine = nib.load(path).affine, header = nib.load(path).header)
        out1.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_AD_DMD_" + tenseur + ".nii.gz")
        
        out2 = nib.Nifti1Image(RD, affine = nib.load(path).affine, header = nib.load(path).header)
        out2.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_RD_DMD_" + tenseur + ".nii.gz")
        
        out3 = nib.Nifti1Image(FA, affine = nib.load(path).affine, header = nib.load(path).header)
        out3.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_FA_DMD_" + tenseur + ".nii.gz")
        
def get_fractions(subjects_path, patient_path):
    
    """
        Parameters
        ----------
        patient_nb : String
            Number of patients.
            
        fractions_all : List of file path in string
            File containing the fractions of one patient for E1 and E2.
    
        Returns
        -------
        List of all the subfile contained in input file fractions. Just a function to get the proper files to work. 
    """
    
    fractions_diamond = nib.load(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions.nii.gz")
    
    fractions_diamond_array = fractions_diamond.get_fdata()
    
    fraction_f0 = np.squeeze(fractions_diamond_array[:,:,:,:,0])
    fraction_f1 = np.squeeze(fractions_diamond_array[:,:,:,:,1])
    fraction_csf = np.squeeze(fractions_diamond_array[:,:,:,:,2])
    
    out_f0 = nib.Nifti1Image(fraction_f0, fractions_diamond.affine, header=fractions_diamond.header)
    out_f0.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f0.nii.gz")
    
    out_f1 = nib.Nifti1Image(fraction_f1, fractions_diamond.affine, header=fractions_diamond.header)
    out_f1.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f1.nii.gz")
    
    out_csf = nib.Nifti1Image(fraction_csf, fractions_diamond.affine, header=fractions_diamond.header)
    out_csf.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_csf.nii.gz")      

def get_cMetrics(subjects_path, patient_path):

    """
        Parameters
        ----------
        subjects_path : String 
            Link of the file in which we are. 
        patient_path : List of strings
            Number of all patients in string ["sub#_E1"] for example.
    
        Returns
        -------
        None. But creation of files containing the wFA, wMD, wAD and wRD for each patient. "w" stands for weigthed.
    """

    metrics = ["FA","MD","AD","RD"]
    
    for metric in metrics :    
        metric_t0   = subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_" + metric + "_DMD_t0.nii.gz"
        
        metric_t1   = subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_" + metric + "_DMD_t1.nii.gz"
         
        fraction_t0 = subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f0.nii.gz"
        
        fraction_t1 = subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_diamond_fractions_f1.nii.gz"
        
        
        cMetric = (nib.load(metric_t0).get_fdata() * nib.load(fraction_t0).get_fdata() + nib.load(metric_t1).get_fdata() * nib.load(fraction_t1).get_fdata())/(nib.load(fraction_t1).get_fdata() + nib.load(fraction_t0).get_fdata())
        
        out = nib.Nifti1Image(cMetric, affine = nib.load(metric_t0).affine, header = nib.load(metric_t0).header)
        out.to_filename(subjects_path + patient_path + "/dMRI/microstructure/diamond/" + patient_path + "_w" + metric + ".nii.gz")


patient = sys.argv[1]         
get_FA_DIAMOND(subjects_path, patient)
get_fractions(subjects_path, patient)
get_cMetrics(subjects_path, patient)