import elikopy 
import elikopy.utils
from elikopy.individual_subject_processing import report_solo


f_path = "/CECI/proj/pilab/PermeableAccess/alcooliques_As2Z4vF8GNv/Pauline_folder/study/"
dic_path="/home/users/q/d/qdessain/Script_python/fixed_rad_dist.mat"
patient_list = ["sub11_E1", "sub11_E2"]
                                   
study = elikopy.core.Elikopy(f_path, slurm=True, slurm_email='pauline.hermans@student.uclouvain.be', cuda=False)

# =============================================================================
# Patient list
# =============================================================================
study.patient_list()

# =============================================================================
# Preprocessing
# =============================================================================
study.preproc(eddy=True,topup=True,denoising=True, reslice=False, gibbs=False, biasfield=False,patient_list_m=patient_list, qc_reg=False, starting_state=None, report=True)


# =============================================================================
# Mask de matière blanche
# =============================================================================
study.white_mask("wm_mask_FSL_T1",patient_list_m=patient_list, corr_gibbs=True, cpus=2, debug=False) # Done wm_mask_FSL_T1, maskType in ["wm_mask_AP", "wm_mask_FSL_T1"]
   
# =============================================================================
# Modèles microstructuraux 
# =============================================================================
study.dti(patient_list_m=patient_list)
study.odf_msmtcsd(num_peaks=2, peaks_threshold=0.25, patient_list_m=patient_list)
study.noddi(patient_list_m=patient_list)
study.diamond(patient_list_m=patient_list)
study.fingerprinting(dic_path, patient_list_m=patient_list)

study.tracking(folder_path = f_path, patient_list_m=patient_list)

# =============================================================================
# Statistiques
# =============================================================================
grp1=[1] # = data_1
grp2=[2] # = data_2

study.regall_FA(grp1=grp1,grp2=grp2, registration_type="-T", postreg_type="-S", prestats_treshold=0.2, cpus=8)

metrics={'_noddi_odi':'noddi','_mf_fvf_tot':'mf'}
study.regall(grp1=grp1,grp2=grp2, metrics_dic=metrics)
study.randomise_all(randomise_numberofpermutation=0,skeletonised=True,metrics_dic=metrics,regionWiseMean=True,cpus=1,slurm_timeout="1:00:00")

# =============================================================================
# Export
# =============================================================================
study.export(tractography=True, raw=False, preprocessing=False, dti=True, noddi=False, diamond=False, mf=False, wm_mask=False, report=False, preprocessed_first_b0=False, patient_list_m=None)
elikopy.utils.merge_all_reports(f_path)
