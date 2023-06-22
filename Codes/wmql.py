import os
import sys 

#os.system("python /CECI/proj/pilab/PermeableAccess/alcooliques_As2Z4vF8GNv/Pauline_folder/Codes/path.py")

from path import perso_path_string


perso_path, excel_path, subjects_path, patients_path, analysis_path, atlas_path, P_folder_path, Freesurfer_path = perso_path_string(on_cluster=True)


sub = sys.argv[1]

if not os.path.exists(P_folder_path+"Data/wmql/"+sub):

  os.makedirs(P_folder_path+"Data/wmql/"+sub)
    


os.system("tract_querier -a "+P_folder_path+"Data/wmql/"+sub+"/new_wmparc_"+sub+".nii.gz -t "+subjects_path+sub+"/dMRI/tractography/"+sub+"_tractogram.trk -q "+P_folder_path+"Codes/wmql/CC_tract.qry -o "+P_folder_path+"Data/wmql/"+sub+"/"+sub)

os.system("tract_querier -a "+P_folder_path+"Data/wmql/"+sub+"/new_wmparc_"+sub+".nii.gz -t "+subjects_path+sub+"/dMRI/tractography/"+sub+"_tractogram.trk -q "+P_folder_path+"Codes/wmql/UF_tract.qry -o "+P_folder_path+"Data/wmql/"+sub+"/"+sub)