#from nilearn.image import resample_img
from skimage.transform import resize
import skimage.transform as skTrans
import nibabel as nib
import numpy as np
import SimpleITK as sitk
import os
data_path = '/proj/Mice_Results'
subject_list = []
for root, dirs, files in os.walk(data_path):
        for name in files:
                if (name == 'Mask_2.nii'):
                        print (root)
                        #root_split = root.split('/')
                        subject_list.append(root)

print (subject_list[3])
for i in range(len(subject_list)):
        #subject_list[i] = data_path + '/' + subject_list[i]
        image1 = nib.load(subject_list[i] + '/Mask_2.nii')
        #image1 = sitk.ReadImage(subject_list[i] + '/mask_resize.nii')
        #print (image1.GetDirection())
        #itk_image = sitk.ReadImage('/home/a2010-venmo/mask_SegSRGAN/SegSRGAN/output_cortex/cortex_332_200_$
        #test_image = np.swapaxes(sitk.GetArrayFromImage(image1), 0, 2).astype('float32')
        test_image =  image1.get_fdata()
        #test_image = sitk.GetArrayFromImage(image1)
        #print (np.amax(test_image)) 
        test_image[test_image > 1] = 1
        var = subject_list[i] + '/Mask_identical_2.nii'
        #test_image_1 = test_image.transpose(2,0,1)
        #mask_image_identical = sitk.GetImageFromArray(test_image_1)
        mask_image_identical = nib.Nifti1Image(test_image, image1.affine, image1.header)
        #print (mask_image_identical.GetDirection())
        #break
        #sitk.WriteImage(mask_image_identical, var)
        nib.save(mask_image_identical, var)
        print (subject_list[i])
        #break
        #new_spacing = [1.544, 1.544 , 1.161]
        #image1 =  image.get_fdata()
        #result1 = sitk.Resample(image1, [290, 290, 198], sitk.Transform(),sitk.sitkNearestNeighbor, image1.GetOrigin(), new_spacing,image1.GetDirection(), 0.0, image1.GetPixelID())
        #result1 = sitk.Resample(image1, [290, 290, 198], sitk.Transform(),sitk.sitkNearestNeighbor$        image2 = nib.Nifti1Image(result1, image.affine, image.header)
        #image2 = nib.Nifti1Image(result1, image1.affine, image1.header)
        #var = subject_list[i] + '/mask_resize.nii'
        #sitk.WriteImage(result1, var)
print (len(subject_list))
