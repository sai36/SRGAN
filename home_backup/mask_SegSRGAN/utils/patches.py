"""
  This software is governed by the CeCILL-B license under French law and
  abiding by the rules of distribution of free software.  You can  use,
  modify and/ or redistribute the software under the terms of the CeCILL-B
  license as circulated by CEA, CNRS and INRIA at the following URL
  "http://www.cecill.info".
  As a counterpart to the access to the source code and  rights to copy,
  modify and redistribute granted by the license, users are provided only
  with a limited warranty  and the software's author,  the holder of the
  economic rights,  and the successive licensors  have only  limited
  liability.
  In this respect, the user's attention is drawn to the risks associated
  with loading,  using,  modifying and/or developing or reproducing the
  software by the user in light of its specific status of free software,
  that may mean  that it is complicated to manipulate,  and  that  also
  therefore means  that it is reserved for developers  and  experienced
  professionals having in-depth computer knowledge. Users are therefore
  encouraged to load and test the software's suitability as regards their
  requirements in conditions enabling the security of their systems and/or
  data to be ensured and,  more generally, to use and operate it in the
  same conditions as regards security.
  The fact that you are presently reading this means that you have had
  knowledge of the CeCILL-B license and that you accept its terms.
"""

import os
import shutil
import time
import logging
import sys
import scipy.ndimage
import numpy as np
import utils.interpolation as inter
import utils.normalization as norm

from itertools import product
from sklearn.feature_extraction.image import extract_patches
from .ImageReader import NIFTIReader
from .ImageReader import DICOMReader
from .utils3d import modcrop3D


import SimpleITK as sitk


def array_to_patches(arr, patch_shape=(3, 3, 3), extraction_step=1, normalization=False):
    # Make use of skleanr function extract_patches
    # https://github.com/scikit-learn/scikit-learn/blob/51a765a/sklearn/feature_extraction/image.py
    """Extracts patches of any n-dimensional array in place using strides.
    Given an n-dimensional array it will return a 2n-dimensional array with
    the first n dimensions indexing patch position and the last n indexing
    the patch content.
    Parameters
    ----------
    arr : 3darray
      3-dimensional array of which patches are to be extracted
    patch_shape : integer or tuple of length arr.ndim
      Indicates the shape of the patches to be extracted. If an
      integer is given, the shape will be a hypercube of
      sidelength given by its value.
    extraction_step : integer or tuple of length arr.ndim
      Indicates step size at which extraction shall be performed.
      If integer is given, then the step is uniform in all dimensions.
    normalization : bool
        Enable normalization of the patches

    Returns
    -------
    patches : strided ndarray
      2n-dimensional array indexing patches on first n dimensions and
      containing patches on the last n dimensions. These dimensions
      are fake, but this way no data is copied. A simple reshape invokes
      a copying operation to obtain a list of patches:
      result.reshape([-1] + list(patch_shape))
    """

    patches = extract_patches(arr, patch_shape, extraction_step)
    patches = patches.reshape(-1, patch_shape[0], patch_shape[1], patch_shape[2])
    # patches = patches.reshape(patches.shape[0], -1)
    if normalization is True:
        patches -= np.mean(patches, axis=0)
        patches /= np.std(patches, axis=0)
    print('%.2d patches have been extracted' % patches.shape[0])
    return patches


def patches_to_array(patches, array_shape, patch_shape=(3, 3, 3)):
    """
    Swicth from the patches to the image
    :param patches: patches array
    :param array_shape: shape of the array
    :param patch_shape: shape of the patches
    :return: array
    """
    # Adapted from 2D reconstruction from sklearn
    # https://github.com/scikit-learn/scikit-learn/blob/51a765a/sklearn/feature_extraction/image.py
    # SyntaxError: non-default argument follows default argument : exchange "array_shape" and "patch_shape"
    patches = patches.reshape(len(patches),*patch_shape)
    i_x, i_y, i_z = array_shape
    p_x, p_y, p_z = patch_shape
    array = np.zeros(array_shape)
    # compute the dimensions of the patches array
    n_x = i_x - p_x + 1
    n_y = i_y - p_y + 1
    n_z = i_z - p_z + 1
    for p, (i, j, k) in zip(patches, product(range(n_x), range(n_y), range(n_z))):
        array[i:i + p_x, j:j + p_y, k:k + p_z] += p
  
    for (i, j, k) in product(range(i_x), range(i_y), range(i_z)):
        array[i, j, k] /= float(min(i + 1, p_x, i_x - i) * min(j + 1, p_y, i_y - j) * min(k + 1, p_z, i_z - k))
    return array


def create_patch_from_df_hr(df,
                            per_cent_val_max,
                            path_save_npy,
                            batch_size,
                            contrast_list,
                            list_res,
                            patch_size,
                            order=3,
                            thresholdvalue=0,
                            stride=20,
                            is_conditional=False,
                            interp='scipy',
                            interpolation_type='Spline',
                            fit_mask=False,
                            image_cropping_method='bounding_box',
                            nb_classe_mask = 0):
    
    data_list = []

    labels_list = []

    path_data_mini_batch = []

    path_labels_mini_batch = []
      
    try:
        os.makedirs(path_save_npy)
        print("Dossier cree")
    
    except OSError:
        logging.error('Unexpected error: the directory named %s already exists', path_save_npy)

    mini_batch = 0
    
    remaining_patch = 0
    
    for i in range(df.shape[0]):
        
        reference_name = df["HR_image"].iloc[i]
        # path HR
        
        label_name = df["Label_image"].iloc[i]
        # path label
        
        
        if fit_mask or (image_cropping_method=='overlapping_with_mask'):
            
            mask_name = df["Mask_image"].iloc[i]
        else : 
            mask_name=None
        
        
        print('================================================================')
        print('Processing image : ', reference_name)
        
        t1 = time.time()
        
        low_resolution_image, reference_image, label_image, mask_image, up_scale, original_LR = create_lr_hr_label(reference_name,
                                                                                                       label_name,
                                                                                                       mask_name,
                                                                                                       list_res[i], 
                                                                                                       interp) #From here, the three images have the same size (see crop in create_lr_hr_label)
        '''#CODE BY SAI FOR SAVING TRAINING IMAGES 
        ref_split = reference_name.split('/')
        low_resolution_image1 = low_resolution_image.transpose(2,1,0)
        low_res1 = sitk.GetImageFromArray(low_resolution_image1)
        low_image_name = '/home/a2010-venmo/train_save_images/' + ref_split[4] + '_low.nii'
        sitk.WriteImage(low_res1, low_image_name)
        reference_image1 = reference_image.transpose(2,1,0)
        ref_res1 = sitk.GetImageFromArray(reference_image1)
        ref_image_name = '/home/a2010-venmo/train_save_images/' + ref_split[4] + '_hr.nii'
        sitk.WriteImage(ref_res1, ref_image_name)
        label_image1 = label_image.transpose(2,1,0)
        lab_res1 = sitk.GetImageFromArray(label_image1)
        lab_image_name = '/home/a2010-venmo/train_save_images/' + ref_split[4] + '_label.nii'
        sitk.WriteImage(lab_res1, lab_image_name)
        print ("Training images saved for ", ref_split[4])
        # mask_image will be None if no mask is fitted. 
        print (low_res1.GetSize())
        print(fit_mask)
        print(image_cropping_method)'''
        
        border_to_keep = border_im_keep(reference_image, thresholdvalue)
        
        #reference_image, low_resolution_image = change_contrast(reference_image, low_resolution_image, contrast_list[i])
        print ("PRINT FOR TESTING", reference_image.shape)
        low_resolution_image = add_noise(low_resolution_image, per_cent_val_max)


        normalized_low_resolution_image, reference_image = norm.Normalization\
            (low_resolution_image, reference_image).get_normalized_image()

        interpolated_image, up_scale = inter.Interpolation(normalized_low_resolution_image, up_scale, order, interp,
                                                           interpolation_type).\
            get_interpolated_image(original_LR)
        print("Imterpolated Image Dimensions",interpolated_image.shape[0],interpolated_image.shape[1],interpolated_image.shape[2])
        if image_cropping_method=='bounding_box' :
            
            print("cropping image with bouding box of coordinates",border_to_keep)
            #label_image, reference_image, interpolated_image, mask_image = remove_border(label_image, reference_image,
                                                                               #interpolated_image,mask_image,border_to_keep)
        
        if (patch_size>interpolated_image.shape[0])|(patch_size>interpolated_image.shape[1]) | (patch_size>interpolated_image.shape[2]) : 
            
            raise AssertionError('The patch size is too large compare to the size on the image')
        
        print(fit_mask)
        print(image_cropping_method)
        hdf5_labels, had5_dataa = create_patches(label_image, reference_image, interpolated_image, mask_image, fit_mask, image_cropping_method, patch_size, stride,nb_classe_mask)
        
        print(hdf5_labels.shape)
        print(fit_mask)
        print(image_cropping_method)
        np.random.seed(0)       # makes the random numbers predictable
        random_order = np.random.permutation(had5_dataa.shape[0])
        had5_dataa = had5_dataa[random_order, :, :, :, :]
        hdf5_labels = hdf5_labels[random_order, :, :, :, :]
        
        if is_conditional:
            
            # list_res[i] = (res_x,res_y,res_z)
            # 1st axis = patch axis
            had5_dataa = np.concatenate((had5_dataa, list_res[i][2]*np.ones_like(had5_dataa)), axis=1)
        
        data_list.append(had5_dataa)
        
        labels_list.append(hdf5_labels)
        
        # Transfer to array
        datas = np.concatenate(np.asarray(data_list))
        datas = datas.reshape(-1,
                              datas.shape[-4],
                              datas.shape[-3],
                              datas.shape[-2],
                              datas.shape[-1])
        
        labels = np.concatenate(np.asarray(labels_list))
        labels = labels.reshape(-1,
                                labels.shape[-4],
                                labels.shape[-3],
                                labels.shape[-2],
                                labels.shape[-1])
                                
        t2 = time.time()
        print("Image tranformation + patch creation and organisation :"+str(t2-t1))
        
        print(fit_mask)
        print(image_cropping_method)

        while datas.shape[0] >= batch_size:
            
            t1 = time.time()
            
            np.save(os.path.join(path_save_npy ,"Datas_mini_batch_"+str(mini_batch)) + ".npy",
                    datas[:batch_size, :, :, :, :])
            
            t2 = time.time()
            
            #print("saving Data array :"+str(t2-t1))
            datas = datas[batch_size:, :, :, :, :]
            data_list = [datas]
            
            t1 = time.time()
            
            np.save(os.path.join(path_save_npy,"Label_mini_batch_" + str(mini_batch) + ".npy"), 
                    labels[:batch_size, :, :, :, :])
            
            t2 = time.time()
            
            #print("saving Label array :" + str(t2-t1))
            
            labels = labels[batch_size:, :, :, :, :]
            labels_list = [labels]

            path_data_mini_batch.append(os.path.join(path_save_npy,"Datas_mini_batch_" + str(mini_batch) + ".npy"))
            
            path_labels_mini_batch.append(os.path.join(path_save_npy,"Label_mini_batch_" + str(mini_batch) + ".npy"))
            
            remaining_patch = datas.shape[0]
            
            mini_batch += 1

    # Label[:,1,:,:,:] : seg , Label[:,0,:,:,:] : HR
    return path_save_npy, path_data_mini_batch, path_labels_mini_batch, remaining_patch


def create_patches(label, hr, interp, mask, fit_mask, image_cropping_method, patch_size, stride,nb_classe_mask):
    
    # Extract 3D patches
    print('Generating training patches ')

    data_patch = array_to_patches(interp, patch_shape=(patch_size, patch_size, patch_size), extraction_step=stride,
                                  normalization=False)
    # image interp dim = (nb_patch,patch_size,patch_size,patch_size)
    print('for the interpolated low-resolution patches of training phase.')

    label_hr_patch = array_to_patches(hr, patch_shape=(patch_size, patch_size, patch_size), extraction_step=stride,
                                      normalization=False)
    # image hr dim = (nb_patch,patch_size,patch_size,patch_size)

    print('for the reference high-resolution patches of training phase.')

    label_cortex_patch = array_to_patches(label, patch_shape=(patch_size, patch_size, patch_size),
                                          extraction_step=stride, normalization=False)
    # image seg dim = (nb_patch,patch_size,patch_size,patch_
    # size)

    print('for the Cortex Labels patches of training phase.')
    
    if fit_mask or (image_cropping_method=='overlapping_with_mask'):
    
        mask_patch = array_to_patches(mask, patch_shape=(patch_size, patch_size, patch_size),
                                              extraction_step=stride, normalization=False)
        binary_mask_patch = mask_patch.copy()
        binary_mask_patch[binary_mask_patch!=0] = 1
        # image seg dim = (nb_patch,patch_size,patch_size,patch_
        # size)
    
        print('for the mask Labels patches of training phase.')
   
    # here, the dimension of the patch are [i,patch_size_patch_size,patch_size]
    
    if image_cropping_method == "overlapping_with_mask":
        
        # remove patch where overlapping with mask is less than 50% 
        
        data_patch,label_hr_patch,label_cortex_patch,mask_patch = remove_patch_based_on_overlapping_with_mask(data_patch, 
                                                                                                              label_hr_patch,
                                                                                                              label_cortex_patch,
                                                                                                              binary_mask_patch)
    if fit_mask :
        
        mask_patch = np.array([[mask_patch[i]==j for j in range(nb_classe_mask)] for i in range(mask_patch.shape[0])])
        
        # Concatenate hr patches and Cortex segmentation : hr patches in the 1st channel, Segmentation the in 2nd channel and mask on the 3rd
        label_hr_patch = np.expand_dims(label_hr_patch,axis=1)
        label_cortex_patch = np.expand_dims(label_cortex_patch,axis=1)
        
        hdf5_labels = np.concatenate((label_hr_patch, label_cortex_patch,mask_patch),axis=1)
        # first dim = patch ex : hdf5_labels[0,0,:,:,:] = hr first patch
        # et hdf5_labels[0,1,:,:,:] = label first patch
        
    else :   
        
        # Concatenate hr patches and Cortex segmentation : hr patches in the 1st channel and Segmentation the in 2nd channel
        hdf5_labels = np.stack((label_hr_patch, label_cortex_patch))
        # hdf5_labels[0] = label_hr_patch et 1=label_cortex_patch

        hdf5_labels = np.swapaxes(hdf5_labels, 0, 1)
        # first dim = patch ex : hdf5_labels[0,0,:,:,:] = hr first patch
        # et hdf5_labels[0,1,:,:,:] = label first patch
    
    # n-dimensional Caffe supports data's form : [numberOfBatches,channels,heigh,width,depth]
    # Add channel axis !
    hdf5_data = data_patch[:, np.newaxis, :, :, :]

    return hdf5_labels, hdf5_data

def remove_patch_based_on_overlapping_with_mask(data_patch,label_hr_patch,label_cortex_patch,mask_patch):
    
    patches_to_keep = [np.mean(mask_patch[i,:,:,:])>0.5 for i in range(mask_patch.shape[0])]
    
    print("after overlapping with mask",np.sum(patches_to_keep),"have been kept on the",len(patches_to_keep),"initial")
    
    data_patch = data_patch[patches_to_keep,:,:,:]
    label_hr_patch = label_hr_patch[patches_to_keep,:,:,:]
    label_cortex_patch = label_cortex_patch[patches_to_keep,:,:,:]
    mask_patch = mask_patch[patches_to_keep,:,:,:]
    
    return data_patch,label_hr_patch,label_cortex_patch,mask_patch
    
    

                  
def border_im_keep(hr, threshold_value):
    dark_region_box = np.where(hr > threshold_value)
    border = ((np.min(dark_region_box[0]), np.max(dark_region_box[0])),
              (np.min(dark_region_box[1]), np.max(dark_region_box[1])),
              (np.min(dark_region_box[2]), np.max(dark_region_box[2])))

    return border


def remove_border(label, hr, interp,mask, border):
    hr = hr[border[0][0]:border[0][1], border[1][0]:border[1][1], border[2][0]:border[2][1]]
    label = label[border[0][0]:border[0][1], border[1][0]:border[1][1], border[2][0]:border[2][1]]
    interp = interp[border[0][0]:border[0][1], border[1][0]:border[1][1], border[2][0]:border[2][1]]
    if mask is not None : 
        mask = mask[border[0][0]:border[0][1], border[1][0]:border[1][1], border[2][0]:border[2][1]]
    return label, hr, interp,mask


def add_noise(lr, per_cent_val_max):
    
    sigma = per_cent_val_max*np.max(lr)

    lr = lr + np.random.normal(scale=sigma, size=lr.shape)
    
    lr[lr < 0] = 0

    return lr


def create_lr_hr_label(reference_name, label_name,mask_name,new_resolution, interp):

    # Read the reference SR image
    if reference_name.endswith('.nii') or reference_name.endswith('.hdr'):
        reference_instance = NIFTIReader(reference_name)
    elif os.path.isdir(reference_name):
        reference_instance = DICOMReader(reference_name)

    reference_image = reference_instance.get_np_array()
    
    constant = 2*np.sqrt(2*np.log(2))
    # As Greenspan et al. (Full_width_at_half_maximum : slice thickness)
    sigma_blur = new_resolution/constant

    # Get resolution to scaling factor
    up_scale = tuple(itemb/itema for itema, itemb in zip(reference_instance.itk_image.GetSpacing(), new_resolution))

    # Modcrop to scale factor
    reference_image = modcrop3D(reference_image, up_scale)

    # Read the labels image
    if label_name.endswith('.nii') or label_name.endswith('.hdr'):
        label_instance = NIFTIReader(label_name)
    elif os.path.isdir(label_name):
        label_instance = DICOMReader(label_name)
        
    label_image = label_instance.get_np_array()
        
    label_image = modcrop3D(label_image, up_scale)
    
    if mask_name is not None : # not none implies we need mask for remove somes patches or fit model for making mask prediction
        # Read the mask image
        if label_name.endswith('.nii') or label_name.endswith('.hdr'):
            mask_instance = NIFTIReader(mask_name)
        elif os.path.isdir(label_name):
            mask_instance = DICOMReader(mask_name)
        
        mask_image = mask_instance.get_np_array()
        
        mask_image = modcrop3D(mask_image, up_scale)
        
    else : 
        
        mask_image=None


    # ===== Generate input LR image =====
    # Blurring
    BlurReferenceImage = scipy.ndimage.filters.gaussian_filter(reference_image, sigma=sigma_blur)

    print('Generating LR images with the resolution of ', new_resolution)

    # Down sampling
    if interp == 'scipy':
        low_resolution_image = scipy.ndimage.zoom(BlurReferenceImage, zoom=(1/float(idxScale) for idxScale in up_scale),
                                                order=0)
        original_LR = None
    elif interp == 'sitk':
        low_resolution_image = BlurReferenceImage[::int(round(up_scale[0])), ::int(round(up_scale[1])), ::int(round(up_scale[2]))]
        original_LR = sitk.GetImageFromArray(np.swapaxes(low_resolution_image, 0, 2))
        original_LR.SetSpacing(new_resolution)
        original_LR.SetOrigin(reference_instance.itk_image.GetOrigin())
        original_LR.SetDirection(reference_instance.itk_image.GetDirection())
    else:
        raise TypeError('Wrong interp value')

    return low_resolution_image, reference_image, label_image, mask_image, up_scale, original_LR


def change_contrast(hr, lr, power):
    hr = hr**power
    lr = lr**power
    
    return hr, lr
