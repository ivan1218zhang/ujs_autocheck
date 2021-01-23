# 实现江苏大学自动健康打卡并部署到云服务器 #
## 环境 ##
+ Python3.6.8
+ selenium+chromedriver+chrome
+ requests
+ tesseract+pytesseract
+ PIL
+ CV2
+ 阿里云ECS云服务器
+ (自行百度如何搭建环境，注意chrome和chromedriver版本对应)
## 实现思路 ##
### 登录 ###
+ 江苏大学的健康打卡系统，保存用户登录信息的cookies只能保留一天，所以没办法做到提取cookies后一劳永逸，所以选择识别验证码并登录来进行打卡。
### 打卡 ###
+ 打卡用带data的post对网站请求
### 定时打卡 ###
+ 循环程序 并用python的time库 到规定时间进行打卡
### 部署到云服务器 ###
+ 服务器安装windows系统 用windows远程桌面链接控制 搭建环境并运行程序
## 使用注意 ##
+ 自行完善id(一卡通学号)和keywords(登录密码) 自己手动打卡一次并复制post的data数据到程序的data={}中