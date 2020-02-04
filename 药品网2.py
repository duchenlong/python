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
    begin = html.find('<div class',start,end)
    begin = html.find('href="',begin,end)
    while begin != -1:
        begin += 6
        over = html.find('"',begin,end)    
        #print(html[begin:over])
        str = html[begin:over]
        
        begin = html.find('href="',begin,end)
        if str.find('javascript') != -1:
            continue
        if str.find('http://yao.xywy.com') == -1:
            url = 'http://yao.xywy.com' + str
        else:
            url = str
        
        img_address.append(url)
        #print(url)
        
    '''
    for each in img_address:
        print(each)
    '''
    return img_address

#提取字符串中的汉字
def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

#文件写入
def file_write(path,informate):
    fp = open(path,'w',encoding = 'utf-8')
    fp.write(informate)
    fp.close()
    
#返回该类图片所有页的网址
def get_allpage(url):
    flag = 0
    if len(url.split('-'))>5:
        flag = 1

    if flag == 0:
        add = url.find('.htm')
        before = url[0:add]
        after = url[add:len(url)]
    else:
        add = url.find('1.htm')
        before = url[0:add-1]
        after = url[add+1:len(url)]
    #print(before,after)
    i = 0
    while True:
        i += 1
        URL = before + '-' + str(i) + after
        
        html = url_open(URL).decode('utf-8')
        if html.find('<div class="tj-docs mt20 pub-warp">') == -1:
            break
        
        start = html.find('<div class="tj-docs mt20 pub-warp">')
        end = html.find('<div class="cb"></div>',start)
        
        #找到该类文件名
        filename_start = html.find('<h2 class',start)
        filename_start = html.find('>',filename_start) + 1
        filename_end = html.find('<',filename_start)
        filename = html[filename_start:filename_end]

        open_file(filename)
        
        img_address = Find_url(start,end,html)
        img_address = list(set(img_address))
        for each in img_address:
            print(each)
        downlode(img_address)
        
        os.chdir('..')

    

#爬取当前网页的图片和信息
def downlode(img_address):
    for each in img_address:
        #如果该网页是一类图片，则重新处理
        if each.find('class') != -1 or each.find('jibing') != -1:
            img_class = get_allpage(each)
            continue
        print(each)
        html = url_open(each).decode('utf_8')
        start = html.find('<div class="pub-warp mt20">')
        end = html.find('<script>',start)

        infor = re.search(r'title="[\u4e00-\u9fa5].+?".?',html[start:end])
        if  not infor:
            continue
        filename = infor.group()
        filename = find_chinese(filename)
        '''
        if os.path.exists(filename):
            print(filename + ' 已存在')
            continue
        '''
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

        file_write(os.getcwd() + '\功能主治.txt',function)
        
        time.sleep(0.2)
        os.chdir('..')

def work(url):
    html = url_open(url).decode('utf-8')
    start = html.find('<div class="index-cons bc w1000 mt20">')
    end = html.find('<div class="links">')
    filename_start = html.find('<h3 class="',start)

    i = 0
    while filename_start != end:
        i += 1
        
        filename_end = html.find('</h3>',filename_start)
        fname = find_chinese(html[filename_start:filename_end])
        nextfile_start = html.find('<h3 class="',filename_end,end)
        print(fname)
        if nextfile_start == -1:
            nextfile_start = end
        
        if i < 4:
            filename_start = nextfile_start
            continue
        
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
