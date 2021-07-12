import os
#import SimpleITK as sitk
import glob, os
import pandas as pd
Image_names = []
Mask_names = []
for file in glob.glob("/proj/Mice_Results/*/*/*.nii"):
	Image_names.append(file)
from skimage.transform import resize
import skimage.transform as skTrans
#import nibabel as nib
import numpy as np
import SimpleITK as sitk
import os
for file in Image_names:
	image = sitk.ReadImage(file)
	new_spacing = [0.875, 0.875, 2.5]
	reference_image = sitk.Resample(image, [256, 256, 64], sitk.Transform(),sitk.sitkNearestNeighbor, image.GetOrigin(), new_spacing, image.GetDirection(), 0.0, image.GetPixelID())
	#image.SetSpacing([0.875, 0.875, 2.5])
	save_name = file.split('.')
	save_name_1 = save_name[0] + '_2.nii'
	print (save_name_1)
	#var = subject_list[i] + '/Mask_spacing.nii'
	sitk.WriteImage(reference_image, save_name_1)

'''
data_path = '/proj/SegSRGAN/GoldAtlasCroppedNifti'
subject_list = []
for root, dirs, files in os.walk(data_path):
        for name in files:
                if (name == 'Binary Mask.nii'):
                        root_split = root.split('/')
                        subject_list.append( root_split[-1])
'''
'''
for i in range(len(subject_list)):
        subject_list[i] = data_path + '/' + subject_list[i]
        image = sitk.ReadImage(subject_list[i] + '/Binary Mask.nii')
        #itk_image = sitk.ReadImage('/home/a2010-venmo/mask_SegSRGAN/SegSRGAN/output_cortex/cortex_332_200_$
        #test_image = np.swapaxes(sitk.GetArrayFromImage(image1), 0, 2).astype('float32')
        #print (np.amax(test_image)) 
        test_image[test_image > 1] = 1
        var = subject_list[i] + '/mask_identical.nii'
        mask_image_identical = sitk.GetImageFromArray(test_image)
        sitk.WriteImage(mask_image_identical, var)
        #image = nib.load(subject_list[i] + '/Image.nii')
        image.SetSpacing([0.875, 0.875, 2.5])
        var = subject_list[i] + '/Mask_spacing.nii'
        sitk.WriteImage(image, var)
        #image1 = np.swapaxes(sitk.GetArrayFromImage(image), 0, 2).astype('float32')
        #image1 =  image.get_fdata()
        result1 = sitk.Resample(image1, [256, 256, 64], sitk.Transform(),sitk.sitkNearestNeighbor, image.GetOrigin(), new_spacing, image.GetDirection(), 0.0, image.GetPixelID())
        #result1 = sitk.Resample(image1, [256, 256, 64], sitk.Transform(),sitk.sitkNearestNeighbor, image1.GetOrigin(), new_spacing,image1.GetDirection(), 0.0, image1.GetPixelID())
        image2 = nib.Nifti1Image(result1, image1.affine, image1.header)
        var = subject_list[i] + '/Image_spacing.nii'
        nib.save(image2, var)
        #sitk.WriteImage(result1, var)'''
print (len(subject_list))
