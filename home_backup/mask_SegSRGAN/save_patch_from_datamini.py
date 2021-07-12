import numpy as np
import SimpleITK as sitk
train_Path_Datas_mini_batch = '/proj/SegSRGAN/temp_training/train_mini_batch/Datas_mini_batch_1.npy'
train_Labels_mini_batch = '/proj/SegSRGAN/temp_training/train_mini_batch/Label_mini_batch_1.npy'

lr_patch_1 = np.load(train_Path_Datas_mini_batch)[1, 0, :, :, :]
lr_patch_1 = lr_patch_1.transpose(2,1,0)
low_res1 = sitk.GetImageFromArray(lr_patch_1)
sitk.WriteImage(low_res1, '/home/a2010-venmo/train_patch/low_res_patch_2.nii')

hr_patch_1 = np.load(train_Labels_mini_batch)[1,0,:, :, :]
hr_patch_1 = hr_patch_1.transpose(2,1,0)
hr_res1 = sitk.GetImageFromArray(hr_patch_1)
sitk.WriteImage(hr_res1, '/home/a2010-venmo/train_patch/hr_patch_2.nii')

lab_patch_1 = np.load(train_Labels_mini_batch)[1,1,:, :, :]
lab_patch_1 = lab_patch_1.transpose(2,1,0)
lab_res1 = sitk.GetImageFromArray(lab_patch_1)
sitk.WriteImage(lab_res1, '/home/a2010-venmo/train_patch/lab_patch_2.nii')

lr_patch_1 = np.load(train_Path_Datas_mini_batch)[20, 0, :, :, :]
lr_patch_1 = lr_patch_1.transpose(2,1,0)
low_res1 = sitk.GetImageFromArray(lr_patch_1)
sitk.WriteImage(low_res1, '/home/a2010-venmo/train_patch/low_res_patch_3.nii')

hr_patch_1 = np.load(train_Labels_mini_batch)[20,0,:, :, :]
hr_patch_1 = hr_patch_1.transpose(2,1,0)
hr_res1 = sitk.GetImageFromArray(hr_patch_1)
sitk.WriteImage(hr_res1, '/home/a2010-venmo/train_patch/hr_patch_3.nii')

lab_patch_1 = np.load(train_Labels_mini_batch)[20,1,:, :, :]
lab_patch_1 = lab_patch_1.transpose(2,1,0)
lab_res1 = sitk.GetImageFromArray(lab_patch_1)
sitk.WriteImage(lab_res1, '/home/a2010-venmo/train_patch/lab_patch_3.nii')


