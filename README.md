# 实现江苏大学自动健康打卡并部署到云服务器 #
## 环境 ##
+ Python3.6.8
+ selenium+chromedriver
+ requests
+ tesseract+pytesseract
+ PIL
+ CV2
## 实现思路 ##
+ 登录
### 江苏大学的健康打卡系统，保存用户登录信息的cookies只能保留一天，所以没办法做到提取cookies后一劳永逸，所以选择识别验证码并登录来进行打卡。 ###
+ 打卡
### 打卡用带data的post对网站请求 ###
+ 定时打卡
### 循环程序 并用python的time库 到规定时间进行打卡 ###
