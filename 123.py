import urllib.request as request
import os
import random
import time

def get_img(length,width):
    ##设置猫的图片的长度和宽度的网址
    html = "http://placekitten.com/" + str(length) + "/" + str(width)
    return html

def find_img():
    img_address = []
    
    length = 380
    width = 430

    ##设置猫图片的长度和宽度
    for j in range(3):
        length += j*100
        width += j*100
        for i in range(1,9):
            img_address.append(get_img(length+i*10,width+i*10))
            
    ##print(img_address)
    downlode_cat(img_address)

def downlode_cat(img_address):

    for ench in img_address:
        req = request.Request(ench)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0')
        
        response = request.urlopen(req)
        cat_img = response.read()

        length = str(ench.split('/')[-2])
        width = str(ench.split('/')[-1])
        
        name = 'cat_' + length + '_' + width + '.jpg'
        print(name)
        time.sleep(0.5)
        with open(name,'wb') as f:
            f.write(cat_img)


os.mkdir('cat5') ##创建一个cat的文件夹
os.chdir('cat5')##将新建的cat文件夹移动到当前目录下
find_img()
