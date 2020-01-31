import urllib.request as request
import datetime
import time
import random
import base64
import os

def url_open(url):
    req = request.Request(url)
    '''
    user = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134']
                       # 构建请求头
    req.add_header('User-Agent',random.choice(user))
    '''
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36')
    response = request.urlopen(req)
    html = response.read()
    time.sleep(0.05) #睡眠0.05s
    return html

#找到网页开始的名字
def get_page(url):
    html = url_open(url).decode('utf-8')
    a = html.find('current-comment-page') + 23
    b = html.find(']',a)

    #print(html[a:b])
    return html[a:b]

##网址的解密
def get_code(num):
    
    date = datetime.datetime.now().strftime('%Y%m%d')   # 获取当前日期并转换成字符串
    
    code = '%s-%s' % (date, num)                        # 连接成需要加密的字符串
    code = date + '-' + num
    bin_code = code.encode('utf-8')                     # 加密字符串
    
    md5_code = base64.b64encode(bin_code).decode()
    return md5_code

#查找图片的网址
def find_img(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []

    a = html.find('img src=')
    while a != -1:
        
        b = html.find('.jpg',a,a + 255)

        if b != -1:
            img_addrs.append('http:' + html[a+9:b+4])
        else:
            b = a + 9
            
        a = html.find('img src=',b)
        
    '''
    for ench in img_addrs:
        print(ench)
    '''
    return img_addrs

def save_imgs(folder,img_addrs):
    i = 0
    for ench in img_addrs:
        filename = ench.split('/')[-1]

        print(filename)
        with open(filename,'wb') as f:
            img = url_open(ench)
            f.write(img)

#建立文件夹，并切换到该文件夹的目录下
def set_mkdir(folder):
    isExists = os.path.exists(folder)
    if not isExists:
        print('创建目录 ')
        os.mkdir(folder) #创建目录
    else:
        print('目录已存在 ')
        
    os.chdir(folder) #切换到创建的文件夹
    print('即将进行图片保存！' + '-->' + folder)
        
def downlode(folder,pages = 20):
    set_mkdir(folder)
        
    url = 'http://jandan.net/' + folder + '/'
    ##print(url)
    page_num = int(get_page(url))

    for i in range(pages):
        page_num -= 1
        page_url = url + str(get_code(str(page_num))) + '/#comments'

        img_addrs = find_img(page_url)
        save_imgs(folder,img_addrs)

if __name__ == '__main__':
    address = ['zoo','ooxx','pic']
    for ench in address:
        
        downlode(ench)
        os.chdir('..')
