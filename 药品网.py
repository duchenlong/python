import urllib.request
import random
import time
import os
import re

#打开网址
def url_open(url):
    req = urllib.request.Request(url)
    user = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0']
    req.add_header('User-Agent',random.choice(user))
    response = urllib.request.urlopen(req)
    html = response.read()
    time.sleep(0.05)
    return html

def open_file(filename):
    isExists = os.path.exists(filename)

    if not isExists:
        print('正在创建 ' + filename + ' 目录')
        os.mkdir(filename)
    else:
        print(filename + ' 目录已经存在')

    os.chdir(filename) #切换到创建的文件夹下
    print('即将进行图片保存 --> ' + filename)

#获取文件的目录
def Find_url(start,end,html):
    img_address = []
    begin = html.find('href="',start,end) + 6
    begin = html.find('href="',begin,end)
    while begin != -1:
        begin += 6
        over = html.find('"',begin,end)
        #print(html[begin:over])
        url = 'http://yao.xywy.com' + html[begin:over]
        img_address.append(url)
        #print(url)
        begin = html.find('href="',begin,end)
    

    return img_address

#提取字符串中的汉字
def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

#文件写入
def file_write(informate,path):
    fp = open(path,'w',encoding = 'utf-8')
    fp.write(informate)
    fp.close()

def downlode(img_address):
    for each in img_address:
        html = url_open(each).decode('utf_8')
        start = html.find('<div class="pub-warp mt20">')
        end = html.find('<script>',start)
        
        filename = re.search(r'title="[\u4e00-\u9fa5].+?".?',html[start:end]).group()
        filename = find_chinese(filename)

        open_file(filename)

        begin = html.find('src="',start)
        while begin != -1:
            over = html.find('"',begin+5,end)
            img_url = html[begin+5:over]
            name = img_url.split('/')[-1]
            print(name)
            with open(name,'wb') as fp:
                fp.write(url_open(img_url))
            begin = html.find('src="',over,end)
            #print(begin)
        begin = html.find('<div class="d-info fl ml20 mt20">',end)
        src = html.find('<dt>功能主治：</dt>',begin)
        function_str = html.find('">',src)
        function_end = html.find('</dd>',function_str)
        function = html[function_str+2:function_end]

        file_write(os.getcwd() + '.txt',function)
        
        time.sleep(1)
        os.chdir('..')

def work(url):
    html = url_open(url).decode('utf-8')
    start = html.find('<div class="index-cons bc w1000 mt20">')
    end = html.find('<div class="links">')
    filename_start = html.find('<h3 class="',start)
    while filename_start != end:
        filename_end = html.find('</h3>',filename_start)
        fname = find_chinese(html[filename_start:filename_end])
        nextfile_start = html.find('<h3 class="',filename_end,end)

        if nextfile_start == -1:
            nextfile_start = end
        open_file(fname)
        
        img_url = Find_url(filename_start,nextfile_start,html)
        
        downlode(img_url)
        
        os.chdir('..')
        
        filename_start = nextfile_start

        
        

if __name__ == '__main__':
    url = 'http://yao.xywy.com/'
    filename = '药品'

    open_file(filename)

    work(url)

    os.chdir('..')
