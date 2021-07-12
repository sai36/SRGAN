import os
#import SimpleITK as sitk
import glob, os
file_names = []
for file in glob.glob("/proj/Mice_Results/*/*/Image.nii"):
    print(file)
