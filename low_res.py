from ImageReader import NIFTIReader
from ImageReader import DICOMReader
from utils3d import modcrop3D
import scipy.ndimage
import numpy as np
import SimpleITK as sitk

new_resolution = [3, 3, 2.5]
reference_instance = NIFTIReader('/proj/SegSRGAN/GoldAtlasMHD/1_04_P/image_resize.nii')
reference_image = reference_instance.get_np_array()
constant = 2*np.sqrt(2*np.log(2))
sigma_blur = new_resolution/constant
up_scale = tuple(itemb/itema for itema, itemb in zip(reference_instance.itk_image.GetSpacing(), new_resolution))
print (up_scale)
print (reference_image.shape)
reference_image = modcrop3D(reference_image, up_scale)
print (reference_image.shape)
BlurReferenceImage = scipy.ndimage.filters.gaussian_filter(reference_image, sigma=sigma_blur)
print (BlurReferenceImage.shape)
low_resolution_image = scipy.ndimage.zoom(BlurReferenceImage, zoom=(1/float(idxScale) for idxScale in up_scale),
                                                order=0)
print (low_resolution_image.shape)
low_resolution_image = low_resolution_image.transpose(2,1,0)
low_res = sitk.GetImageFromArray(low_resolution_image)
low_res.SetSpacing([3,3,2.5])
print (low_res.GetSpacing())
sitk.WriteImage(low_res, '/home/a2010-venmo/low_res_1_04.nii')
