# autotable
防控师生健康日报表
填完发邮箱通知

# 依赖
requests
# 配置
1. ~~无依赖~~
~~`pip install requests`~~

2. ~~sourcemail填你自己的邮箱~~
3. ~~sourcemailauthcode是对应的授权码，如果是qq邮箱需要发短信得到授权码，取决于哪个平台的邮箱,详情请看[用QQ邮箱发送邮件](https://blog.csdn.net/Momorrine/article/details/79881251)~~
4. batch数组是需要填报的学号以及密码~~，和他的邮箱，填完后会发邮件到这个邮箱,无论是否填报成功都会发送邮件~~

5. 定时任务


  * 第一种方法 放各种云(自己软路由也行)上面装好crontab后输入
  `crontab -e`  
  输入  
  `0 3 * * * python path/to/autotable.py #每天03:00分运行,错峰`  
  
  * 第二种方法 如果你能坚持每天开电脑学da习ji  
  就在这个路径创建autotable.vbs文件  
  "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"  
  并输入  
  ``` vbs
  SET objShell = WScript.CreateObject("WScript.Shell")
  SHOWWINDOW = 0 'change 0 to 1 to show the CMD prompt
  objShell.Run """path\to\python.exe"""" path\to\autotable.py """, SHOWWINDOW'
  ```
