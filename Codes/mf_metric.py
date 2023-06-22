# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:52:44 2023

@author: Pauline

Compute MF metric maps
"""


import nibabel as nib
import sys
from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=False)

def f0_f1_to_ftot(subjects_path, p):
  
    
  # =============================================================================
  # MF
  # =============================================================================
  metric_mf = ["_mf_frac_f0",
               "_mf_frac_f1",
               "_mf_fvf_f0",
               "_mf_fvf_f1"]

      
  path_f0 = subjects_path + p + "/dMRI/microstructure/mf/" + p + metric_mf[0] + ".nii.gz"
  
  path_f1 = subjects_path + p + "/dMRI/microstructure/mf/" + p + metric_mf[1] + ".nii.gz"
  
  path_fvf_f0 = subjects_path + p + "/dMRI/microstructure/mf/" + p + metric_mf[2] + ".nii.gz"
  
  path_fvf_f1 = subjects_path + p + "/dMRI/microstructure/mf/" + p + metric_mf[3] + ".nii.gz"
  
  f0 = nib.load(path_f0)   
  
  f1 = nib.load(path_f1)   
  
  fvf_f0 = nib.load(path_fvf_f0)   
  
  fvf_f1 = nib.load(path_fvf_f1)    
  
  ff =   f0.get_fdata() + f1.get_fdata()
  
  wfvf = ((f0.get_fdata()*fvf_f0.get_fdata()) + (f1.get_fdata()*fvf_f1.get_fdata()))/(f0.get_fdata() + f1.get_fdata())
  
  ou = nib.Nifti1Image(ff, affine = f0.affine, header = f0.header)
  ou.to_filename(subjects_path + p + "/dMRI/microstructure/mf/" + p + "_mf_frac_ftot.nii.gz")
  
  out = nib.Nifti1Image(wfvf, f0.affine, header = f0.header)
  out.to_filename(subjects_path + p + "/dMRI/microstructure/mf/" + p + "_mf_wfvf.nii.gz")

  # =============================================================================
  # DMD
  # =============================================================================
  metric_dmd = ["_diamond_fractions_f0",
                "_diamond_fractions_f1"]
  
  path_f0 = subjects_path + p + "/dMRI/microstructure/diamond/" + p + metric_dmd[0] + ".nii.gz"
  path_f1 = subjects_path + p + "/dMRI/microstructure/diamond/" + p + metric_dmd[1] + ".nii.gz"
 
  f0 = nib.load(path_f0)   
  f1 = nib.load(path_f1)      
 
  ff = f0.get_fdata()+ f1.get_fdata()
 
  out1 = nib.Nifti1Image(ff, affine = f0.affine, header = f0.header)
  out1.to_filename(subjects_path + p + "/dMRI/microstructure/diamond/" + p + "_diamond_fractions_ftot.nii.gz")
  
patient = sys.argv[1]         
f0_f1_to_ftot(subjects_path, patient)