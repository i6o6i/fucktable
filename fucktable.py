from datetime import datetime 
import smtplib
from email.mime.text import MIMEText
from urllib import parse, request, error
import json
import re
from pprint import pprint
import code

#utils
def posturlencode(url, data, headers={}):
    body=parse.urlencode(data).encode()   
    req=request.Request(url,body,method='POST')
    req.add_header('Content-Length', len(body))
    for k, v in headers.items():
        req.add_header(k, v)
    
    res=request.urlopen(req)
    return res

def postrawdata(url, data, headers):
    req=request.Request(url,data,method='POST')
    req.add_header('Content-Length', len(data))
    for k, v in headers.items():
        req.add_header(k, v)
    
    res=request.urlopen(req)
    return res

def get(url,params={}, headers={}):
    querystr=parse.urlencode(params)
    req=request.Request(f"{url}?{querystr}")
    for k, v in headers.items():
        req.add_header(k, v)
    res=request.urlopen(req)
    return res

#发送邮箱
#sourcemail='myemail@qq.com'
#sourcemailauthcode= 'authcodeOfmyemail'
Test=0
test_data={}

batch =[
        {
            #学号及密码
            'studentid':'myid',
            'passwd':'mypasswd',
            '''
            #通知邮箱
            'infoemail': 'myemail@qq.com'
            '''
            }
        ]
#同伴互助
if Test == 0 :
    batch.extend([
            {
                #基友学号及密码
                'studentid':'your_friends_id',
                'passwd':'your_friends_passwd',
                '''
                #基友邮箱
                'infoemail': 'hisemail'
                '''
                }
    ])

for i in batch:
    studentid=i['studentid']
    passwd=i['passwd']
    Headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'}
    #登录拿PHPSESSID
    res=get("https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html",headers=Headers)    
    token = re.search(r'(?<=var token = )"(\w+)";', res.read().decode()).group(1)
    phpsessid=re.search(r'PHPSESSID=([^;]*);',res.getheader('Set-Cookie')).group(1)
    Headers['Cookie'] = f'PHPSESSID={phpsessid};'
    
    #拿到authorization token
    data={
            'username':f'{studentid}',
            'password':f'{passwd}',
            '__token__':f'{token}',
            'wechat_verify':''
         }         
    res=posturlencode(
            "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html",
            data,
            Headers
            ).read().decode()    
    url = json.loads(res)['info']
    res=get(url)    
    access_token=re.search('access_token=(.*)',res.url).group(1)
    print(access_token)
    
    #拿到基本信息并处理表单
    Headers['authorization']=f"Bearer {access_token}"
    res=get('https://yqfk.dgut.edu.cn/home/base_info/getBaseInfo',headers=Headers).read().decode()
    data=json.loads(res)['info']
    data['confirm'] = 1
    data.pop('whitelist',None)
    data.pop('importantAreaMsg',None)
    data.pop('msg',None)
    #测试脚本用
    if Test == 1:
        for ( key, value ) in test_data.items():
            if key not in data:
                print("addinfo.data missing field:", key)
            else:
                print(f"addinfo.data[{key}]:{data[key]}\n",f"test_data[{key}]:{value}")
    data=json.dumps(data).encode()
    
    #FUCK THE TABLE
    Headers['Content-Type'] = 'application/json; charset=utf-8'
    try:
        res=postrawdata('https://yqfk.dgut.edu.cn/home/base_info/addBaseInfo', data, headers=Headers).read().decode()
    except error.HTTPError as e:
        res=e.read().decode()
        pass
    print(i['studentid'],datetime.now().strftime("%Y-%m-%d %H:%M"),json.loads(res)['message'])

'''
    user = sourcemail
    password = sourcemailauthcode

    msg = MIMEText(f"{json.loads(res)['message']}")
    msg['Subject']='今日填报情况'
    msg['From'] = sourcemail
    msg['To'] = i['infoemail']

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(user, password)
        server.sendmail(sourcemail, i['infoemail'], msg.as_string('utf-8'))

        print('Email sent!')
    except:
        print('Somthing went wrong...')
    finally:
        server.quit()
'''
