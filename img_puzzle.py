import os
import cv2
import numpy as np
import math

# set your imgs folder path here
imgs_path='puzzle_imgs'

# set your target image here
target_img_path='target.jpg'

# set your result image name here
res_img_path='res1.png'

# set how many row and columns of images you want to have
row=51
column=51

def read_path(file_pathname):
    imgs=[]
    for filename in os.listdir(file_pathname):
        img = cv2.imread(file_pathname+'/'+filename)
        imgs.append(img)
    return imgs

def resize_imgs(imgs, h, w):
    res=[]
    for img in imgs:
        new_img=cv2.resize(img,(w,h),interpolation=cv2.INTER_AREA)
        res.append(new_img)
    return res

def avg_channel(imgs):
    res=[]
    for img in imgs:
        mean=cv2.mean(img)
        res.append(mean[0:3])
    return res

def square_error(a,b):
    total=0
    for i in range(len(a)):
        total+=abs(a[i]-b[i])**1.2
    return total

def choose_img(target_avg, imgs_avg, imgs):
    lowest_se=math.inf
    lowest_se_index=None
    for i, img in enumerate(imgs_avg):
        se=square_error(img,target_avg)
        if se<lowest_se:
            lowest_se_index=i
            lowest_se=se
    return lowest_se_index

def combine_imgs(imgs):
    row_imgs=[]
    for i in range(len(imgs)):
        row_img=cv2.hconcat(imgs[i])
        row_imgs.append(row_img)
    return cv2.vconcat(row_imgs)

imgs=read_path(imgs_path)
target_img=cv2.imread(target_img_path)
print('img loaded')

img_height=target_img.shape[0]//row
img_width=target_img.shape[1]//column

imgs=resize_imgs(imgs,img_height,img_width)
print('resize finished')

imgs_avg_channel=avg_channel(imgs)
print('avg finished')

imgs_matrix=[]
index_list=[]
for i in range(row):
    for j in range(column):
        index_list.append([i,j])
np.random.shuffle(index_list)

count=0
imgs_matrix = [[0 for _ in range(column)] for _ in range(row)]
for pos in index_list:
    i,j=pos[0],pos[1]
    x1=j*img_width
    x2=(j+1)*img_width
    y1=i*img_height
    y2=(i+1)*img_height

    region=target_img[y1:y2,x1:x2]
    target_avg_channel_per_row=np.average(region,axis=0)
    target_avg_channel=np.average(target_avg_channel_per_row,axis=0)
    nearest_img_index=choose_img(target_avg_channel,imgs_avg_channel,imgs)

    imgs_matrix[i][j]=imgs[nearest_img_index]
    del imgs[nearest_img_index]
    del imgs_avg_channel[nearest_img_index]

    count+=1
    if count%100==0:
        print('finished choosing '+str(count)+' indexs')
print('puzzle choosing finished')

res_img=combine_imgs(imgs_matrix)
print('image combining finished')

cv2.imshow('test',res_img)
cv2.waitKey(0)

choose=input('do you want to save the image y/n \n')
while choose not in ('y','n','Y','N'):
    choose=input('input error, please type y or n \n')
if choose=='y':
    cv2.imwrite(res_img_path,res_img)