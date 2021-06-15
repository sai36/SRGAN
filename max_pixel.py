import SimpleITK as sitk
import numpy as np
itk_image = sitk.ReadImage('/proj/SegSRGAN/GoldAtlasMHD/1_04_P/mask_identical.nii')
test_image = np.swapaxes(sitk.GetArrayFromImage(itk_image), 0, 2).astype('float32')
print (np.amax(test_image))
print(itk_image.GetSize())
print(test_image.shape)
