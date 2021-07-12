import SimpleITK as sitk
itk_image = sitk.ReadImage("/home/student_project/Thesis_project/image1.nii")
print (type(itk_image[:,:,1]))
