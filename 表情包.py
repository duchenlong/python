import urllib.request
import random
import time
import re
import os

#访问网址
def url_open(url):
    a = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36']
    req = urllib.request.Request(url)
    req.add_header('User-Agent',random.choice(a))
    response = urllib.request.urlopen(req)
    html = response.read()
    time.sleep(0.05)
    return html

#创建一个文件夹，并切换到该文件夹的目录下
def open_file(filename):
    isExists = os.path.exists(filename)
    if not isExists:
        print('正在创建' + filename + '目录')
        os.mkdir(filename)
    else:
        print(filename + '目录以经存在')

    os.chdir(filename)
    print('切换到 ' + filename + '目录')
    print('即将进行图片保存')

#得到图片网址和名字
def find_filename(url,flag):
    html = url_open(url).decode('utf-8')
    name_address = []

    start = html.find('<div class="ui secondary pointing blue menu" id="bqbcategory">')
    end = html.find('</div>',start)
    if flag != 1:
        start = html.find('href=',end)
        end = html.find('<script async',start)

    imformate = html.find('href',start,end)  
    while imformate != -1:   
        over = html.find('>',imformate)
        name_address.append(html[imformate:over])
        start = over
        imformate = html.find('href',start,end)
    
    '''
    for each in name_address:
        print(each)
    '''
    
    return name_address
    
def get_name(each):
    start = each.find('title="') + 7
    end = each.find('-',start)
    if end == -1:
        end = each.find('个表情）',start)

    if end == -1:
        end = each.find('（',start)
    else:
        end += 4

    #print(each[start:end])
    return each[start:end]

def get_url(each):
    start = each.find('href="') + 6
    end = each.find('"',start)
    return  'https://www.fabiaoqing.com' + each[start:end]

#得到该文件夹下所有图片的地址和名字
def get_jpg(html):
    jpg_address = []

    start = html.find('<div class="swiper-wrapper">')
    end = html.find('<script async',start)

    imformate = html.find('href=',start)

    while imformate != -1:
        begin = html.find('data-original="',imformate) + 15
        over = html.find('alt=',begin)
        jpg_address.append(html[begin:over])
        
        start = over
        imformate = html.find('href=',start,end)
    
    '''
    for each in jpg_address:
        print(each)
    '''
    
    return jpg_address

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

#添加图片到当前文件夹     
def add_jpg(jpg_name,jpg_url):
    #print(jpg_name.replace('"','1'))
    jpg_name = find_chinese(jpg_name) + '.jpg'
    print(jpg_name)
    with open(jpg_name,'wb') as f:
        img = url_open(jpg_url)
        f.write(img)
        
        

def downlode(url):
    html = url_open(url).decode('utf-8')

    jpg_address = get_jpg(html)

    for each in jpg_address:
        jpg_name = get_name(each)
        jpg_url = each.split('"')[0]

        add_jpg(jpg_name,jpg_url)

    
    
if __name__ == '__main__':
    file = '表情包'
    open_file(file) #打开文件
    url = 'https://www.fabiaoqing.com/bqb/lists/type'
    name_address = find_filename(url,1)#外层网址和文件名
    for each in name_address:
        name = get_name(each)#分割文件名
        open_file(name)
        
        url = get_url(each)#分割网址
        
        img_address = find_filename(url,2)#内层网址和文件名
        for ele in img_address:
            name = get_name(ele)#分割文件名
            open_file(name)
            url = get_url(ele)#分割网址
            
            downlode(url)#爬取该网址的图片
            
            os.chdir('..')
            
        os.chdir('..')
    
