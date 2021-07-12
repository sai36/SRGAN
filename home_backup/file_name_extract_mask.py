import os
#import SimpleITK as sitk
import glob, os
import pandas as pd
Image_names = []
Mask_names = []
for file in glob.glob("/proj/Mice_Results/*/*/Image.nii"):
    Image_names.append(file)
for file in glob.glob("/proj/Mice_Results/*/*/Mask.nii"):
    Mask_names.append(file)
file_df = pd.DataFrame(Mask_names, Image_names)
file_df.to_csv('temporal_cropped_dgx.csv')

'''
with open('temporal_cropped_dgx.csv','w') as output:
    writer = csv.
    with open('C:/test/output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('Berry')
        all.append(row)

        for row in reader:
            row.append(row[0])
            all.append(row)

        writer.writerows(all)
'''
