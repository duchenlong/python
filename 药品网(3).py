import urllib.request
import urllib.error
import random
import time
import os
import re

#浏览器user agent
def get_useragent():
    user = ['Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/77.0.3865.75 Mobile/13B143 Safari/601.1.46','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0']
    user.append('Mozilla/5.0 (BB10; Touch) AppleWebKit/537.1+ (KHTML, like Gecko) Version/10.0.0.1337 Mobile Safari/537.1+')
    user.append('Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML, like Gecko) Version/7.2.1.0 Safari/536.2+')
    user.append('Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.187 Mobile Safari/534.11+') 
    user.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31')
    user.append('Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36')
    user.append('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.31')
    user.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240')
    user.append('Opera/9.80 (Macintosh; Intel Mac OS X 10.9.1) Presto/2.12.388 Version/12.16')
    user.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/13.10586')
    user.append('Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16')
    user.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')
    user.append('Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920) UCBrowser/10.1.0.563 Mobile')
    user.append('Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
    return user

#打开网址
def url_open(url):
    req = urllib.request.Request(url)
    user = get_useragent()
    
    req.add_header('User-Agent',random.choice(user))
    try:
        response = urllib.request.urlopen(req)
        html = response.read()
    except urllib.error.URLError as err:
        return -1
    
    time.sleep(0.05)   
    return html

#打开文件夹并进入该文件夹
def file_open(filename):
    isExists = os.path.exists(filename)

    if not isExists:
        print('正在创建 ' + filename + ' 目录')
        os.mkdir(filename)
    else:
        print(filename + ' 目录已经存在')

    os.chdir(filename) #切换到创建的文件夹下
    print('即将进行图片保存 --> ' + filename)

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
    while i < 5:
        i += 1
        URL = before + '-' + str(i) + after
        
        html = url_open(URL)
        if html == -1:
            return 
        html = html.decode('utf-8')
        
        if html.find('<div class="tj-docs mt20 pub-warp">') == -1:
            break
        
        start = html.find('<div class="tj-docs mt20 pub-warp">')
        end = html.find('<div class="cb"></div>',start)
        
        #找到该类文件名
        filename_start = html.find('<h2 class',start)
        filename_start = html.find('>',filename_start) + 1
        filename_end = html.find('<',filename_start)
        filename = html[filename_start:filename_end]

        file_open(filename)
        
        img_address = re.findall(r'" href="(.+?\.htm)',html[start:end])
        img_address = list(set(img_address))
        i = 0
        for i in range(len(img_address)):
            img_address[i] = 'http://yao.xywy.com' + img_address[i]
            
        for each in img_address:
            print(each)
        print('______________________')
        downlode(img_address)
        os.chdir('..')
        

    

#爬取当前网页的图片和信息
def downlode(img_address):
    for each in img_address:
        html = url_open(each)
        if html == -1:
            continue
        html = html.decode('utf-8')
        
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
        file_open(filename)

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
        
        time.sleep(1)
        os.chdir('..')
    

def url_get(html,start,end):
    begin = html.find('f14 fb"',start,end) + 9
    while begin != end:
        over = html.find('f14 fb"',begin,end)
        if over == -1:
            over = end
        else:
            over += 9
            
        name = re.search(r'>([\u4e00-\u9fa5]+?)<',html[begin:over])
        if not name:
            continue
        name = find_chinese(name.group())
        #print(name)
        begin = html.find('class',begin)
        
        file_open(name)
        
        url_address = re.findall(r'href="(.+?\.htm)"',html[begin:over])
        for each in url_address:
            each = 'http://yao.xywy.com' + each
            get_allpage(each)
            #print(each)
        
        os.chdir('..')

        begin = over
    '''
    for each in url_address:
        print(each)
        '''

def work(url):
    html = url_open(url)
    if html == -1:
        return 
    html = html.decode('utf-8')
    
    start = html.find('<div class="w1000 bc mt20 pb20 clearfix">')
    start = html.find('<div class="re-con clearfix">',start)
    end = html.find('<script type="text/javascript"',start)
    
    #获取分类的各种类别
    #name = re.findall(r'fn ml10">([\u4e00-\u9fa5]+)</h2>?',html[start:end])
    begin = html.find('fn ml10">',start,end) + 9
    while begin != end:
        over = html.find('fn ml10">',begin,end)
        if over == -1:
            over = end
        else:
            over += 9
            
        name_end = html.find('<',begin)
        name = html[begin:name_end]
        #print(name)
        file_open(name)
        
        url_get(html,begin,over)
        
        os.chdir('..')
        begin = over
    
    

if __name__ == '__main__':
    url = 'http://yao.xywy.com/class.htm'
    filename = '药品分类'

    file_open(filename)

    work(url)

    os.chdir('..')
    
    
