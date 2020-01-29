import urllib.request as request
import urllib.parse
import json


while 1:
    text = input('请输入要翻译的语句  (Q 为退出) --> ')
    if text == 'Q':
        break;
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    data = {}
    data['i']= text
    data['from']= 'AUTO'
    data['to']= 'AUTO'
    data['smartresult']= 'dict'
    data['client']= 'fanyideskweb'
    data['salt']= '15802775501713'
    data['sign']= '815376f0081de6462c49723aeb297b2e'
    data['ts']='1580277550171'
    data['bv']=' ac82ef7db64f4b7be76bd20436beba1f'
    data['doctype']='json'
    data['version']=' 2.1'
    data['keyfrom']= 'fanyi.web'
    data['action']= 'FY_BY_CLICKBUTTION'
    data = urllib.parse.urlencode(data).encode('utf-8')

    response = request.urlopen(url,data)
    html = response.read().decode('utf-8')
    ##print(html)
    target = json.loads(html)
    print(target['translateResult'][0][0]['tgt'])
    ##print(target)
