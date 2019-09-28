from cropper import *
from Classifier import *
import csv
import sys
import os

Lable_List = ["Unknown","TShirt","Pant","Kurtha"]
#uncomment to create csv for testing data
'''
for i in range(1,4):
    for j in range(135,150):
        x = Image_Crop("Images/"+str(i)+"/"+str(j)+".jpg")
        total_list=x.Edge_detection()
        total_list.remove(total_list[-1])
        total_list.append(Lable_List[i])
        Item = [total_list]
        print(total_list)
        with open('Testing1.csv', 'a',newline='') as f:
            writer = csv.writer(f)
            for row in Item:
                writer.writerow(row)
        f.close()
        '''
#uncomment to generate csv file for training data
'''
for i in range(1,4):
    for j in range(1,135):
        x = Image_Crop("Images/"+str(i)+"/"+str(j)+".jpg")
        total_list=x.Edge_detection()
        total_list.remove(total_list[-1])
        total_list.append(Lable_List[i])
        Item = [total_list]
        print(total_list)
        with open('Training1.csv', 'a',newline='') as f:
            writer = csv.writer(f)
            for row in Item:
                writer.writerow(row)
        f.close()
    

'''

#start=""

image =sys.argv[1]
x = Image_Crop(image)
total_list=x.Edge_detection()
color = total_list[-1]
total_list.remove(total_list[-1])

total_list.append(Lable_List[0])

with open("C:/Users/anant/OneDrive/Desktop/Hamro dokan/Hamro dokan/ImageClassificationWithRandomForest1/unknown.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(total_list)
f.close()
total = list()
total.append(color)
total.append(main())
print(total[0],total[1])