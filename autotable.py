import requests
import smtplib
from email.mime.text import MIMEText
from urllib import parse
import json
import re

#发送邮箱
sourcemail='myemail@qq.com'
sourcemailauthcode= 'authcodeOfmyemail'

#同伴互助
batch =[
        {
            #学号及密码
            'studentid':'myid',
            'passwd':'mypasswd',
            #通知邮箱
            'infoemail': 'myemail@qq.com'
            },
        {
            #基友学号及密码
            'studentid':'your_friends_id',
            'passwd':'your_friends_passwd',
            #基友邮箱
            'infoemail': 'hisemail'
            },
        ]

for i in batch:
    studentid=i['studentid']
    passwd=i['passwd']
    s=requests.Session()
    Headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'}
    res=s.get("https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html",headers=Headers)
    token = re.search(r'(?<=var token = )"(\w+)";', res.content.decode()).group(1)
    data={
            'username':f'{studentid}',
            'password':f'{passwd}',
            '__token__':f'{token}',
            'wechat_verify':''
            }
    res=s.post(
            "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html",
            data=data,
            )
    url = 'http://yqfk.dgut.edu.cn/auth/auth'+re.search(r'/login?.*home', res.text).group(0)
    res=s.get(url,allow_redirects=False)
    access_token=re.search('access_token=(.*)',res.headers['Location']).group(1)
    phpsessid=re.search('PHPSESSID=(.*)',res.headers['Set-Cookie']).group(1)
    Headers3={
            "authorization" : f"Bearer {access_token}",
            }

    res=s.get('http://yqfk.dgut.edu.cn/home/base_info/getBaseInfo',headers=Headers3)
    data=json.loads(res.text)['info']
    res=s.post('http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo',json=data,headers=Headers3)

    user = sourcemail
    password = sourcemailauthcode

    msg = MIMEText(f"{json.loads(res.text)['message']}")
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
