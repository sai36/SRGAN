from Function_for_application_test_python3 import segmentation

segmentation(input_file_path = "/proj/SegSRGAN/GoldAtlasMHD/1_04_P/lr_3d_image_resize_4.nii", step = 128,new_resolution = (0.5, 0.5, 3),  path_output_cortex = "/home/a2010-venmo/SegSRGAN/result_folder/output_cortex_4.nii", path_output_hr = "/home/a2010-venmo/SegSRGAN/result_folder1/output_hr_4.nii", weights_path = "/proj/SegSRGAN/snapshot/SegSRGAN_epoch_99", interpolation_type = "NearestNeighbor")

