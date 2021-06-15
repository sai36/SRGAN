#from nilearn.image import resample_img
from skimage.transform import resize
import skimage.transform as skTrans
import nibabel as nib
import numpy as np
import SimpleITK as sitk
import os
data_path = '/proj/SegSRGAN/GoldAtlasCroppedNifti'
subject_list = []
for root, dirs, files in os.walk(data_path):
        for name in files:
                if (name == 'Mask.nii'):
                        root_split = root.split('/')
                        subject_list.append( root_split[-1])

for i in range(len(subject_list)):
        subject_list[i] = data_path + '/' + subject_list[i]
        image1 = nib.load(subject_list[i] + '/Mask.nii')
        test_image =  image1.get_fdata()
        test_image[test_image > 1] = 1
        var = subject_list[i] + '/mask_identical.nii'
        mask_image_identical = nib.Nifti1Image(test_image, image1.affine, image1.header)
        nib.save(mask_image_identical, var)
        print (subject_list[i])

print (len(subject_list))
