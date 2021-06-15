from Function_for_application_test_python3 import segmentation

msg = segmentation(input_file_path = "/home/a2010-venmo/low_res_1_04.nii", step = 20,new_resolution = (1.5,1.5,1.2),  path_output_cortex = "/home/a2010-venmo/mask_SegSRGAN/SegSRGAN/output_cortex/cortex_no_dis_104_180.nii", path_output_hr = "/home/a2010-venmo/mask_SegSRGAN/SegSRGAN/output_hr/hr_no_dis_104_180.nii", path_output_mask = "/home/a2010-venmo/mask_SegSRGAN/output_mask/mask_no_dis_104_180.nii", weights_path = "/proj/SegSRGAN/snapshot_no_dis/SegSRGAN_epoch_180", interpolation_type = "NearestNeighbor")
print (msg)

