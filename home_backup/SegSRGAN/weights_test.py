import h5py
import os
from keras.engine import saving
weights = h5py.File("/proj/SegSRGAN/snapshot/SegSRGAN_epoch_99", 'r')
print(weights)
G = weights[list(weights.keys())[1]]
weight_names = saving.load_attributes_from_hdf5_group(G, 'weight_names')
print (weight_names)
for i in weight_names:
    if 'gen_conv1' in i:
        weight_values = G[i]
    if 'gen_1conv' in i : 
        last_conv = G[i]
    first_generator_kernel = weight_values.shape[4]
    nb_out_kernel = last_conv.shape[4] 
    if nb_out_kernel>2:
        fit_mask = True
        nb_classe_mask = nb_out_kernel-2
        print("The initialize network will fit mask")
    else :
        fit_mask = False
        nb_classe_mask=0
        print("The initialize network won't fit mask")
