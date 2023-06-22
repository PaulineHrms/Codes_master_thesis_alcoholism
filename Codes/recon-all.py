import os
import sys

Patient = sys.argv[1]

os.system("recon-all -s " + Patient +" -i /CECI/proj/pilab/PermeableAccess/alcooliques_As2Z4vF8GNv/alcoholic_study/T1/"+ Patient +"_T1.nii.gz -all")