def modcrop3D(img, modulo):
    import math
    img = img[0:int(img.shape[0] - math.fmod(img.shape[0], modulo[0])), 
              0:int(img.shape[1] - math.fmod(img.shape[1], modulo[1])), 
              0:int(img.shape[2] - math.fmod(img.shape[2], modulo[2]))]
    return img

import numpy as np
import SimpleITK as sitk
img = sitk.ReadImage('/proj/Mice_Results/4/9/Image.nii')
new_resolution = [0.875, 0.875, 2.5]
#reference_image = sitk.Image((256,256,64), img.GetPixelIDValue())
reference_image = sitk.Resample(img, [256, 256, 64], sitk.Transform(),sitk.sitkNearestNeighbor, img.GetOrigin(), new_resolution, img.GetDirection(), 0.0, img.GetPixelID())
print ("Reference Image Dimensions",reference_image.GetSize())
#img.SetPixel(256, 256, 64)
print("Image resolution", img.GetSize())
new_resolution = [1.75, 1.75, 5]
up_scale = tuple(itemb/itema for itema, itemb in zip(img.GetSpacing(), new_resolution))
print (up_scale)
#image_arr = img.get_np_array()
image_arr = np.swapaxes(sitk.GetArrayFromImage(img), 0, 2).astype('float32')
img_cropped = modcrop3D(image_arr, up_scale)
sitk.WriteImage(reference_image, "Reference_Image.nii")
print ("After mod crop dimensions", img_cropped.shape)
