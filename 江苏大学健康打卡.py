# -*- coding: utf-8 -*-
from selenium.webdriver import Chrome
import requests
from time import sleep
from PIL import Image
import cv2 as cv
import pytesseract
import sys
import io
import time

url = "http://yun.ujs.edu.cn/xxhgl/yqsb/grmrsb"
# 学号和密码
id=""
keywords=""
# 自行复制post的data数据 浏览器F12查看post的请求
data = {

}


def recognize_text(image):
    # 边缘保留滤波 去噪
    blur = cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
    # 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    print(f'二值化自适应阈值：{ret}')
    # 识别
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    return text


def get_cookies():
    chrome_driver = Chrome(executable_path='chromedriver.exe')
    chrome_driver.maximize_window()  # 将浏览器最大化
    chrome_driver.get(url)
    chrome_driver.find_element_by_xpath("//input[@placeholder='一卡通号']").send_keys(id)
    chrome_driver.find_element_by_xpath("//input[@placeholder='密码']").send_keys(keywords)
    sleep(2)
    chrome_driver.save_screenshot('printscreen.png')
    x = 1365
    y = 465
    width = 140
    height = 60
    im = Image.open('printscreen.png')
    im = im.crop((x, y, x + width, y + height))
    im.save('save.png')
    src = cv.imread('save.png')
    text = recognize_text(src)
    text = ''.join(filter(str.isalnum, text))
    print(text)
    chrome_driver.find_element_by_xpath("//input[@id='captchaResponse']").send_keys(text)
    chrome_driver.find_element_by_xpath("//button[@type='submit']").click()
    cookies = make_cookies(chrome_driver)
    daka(cookies)


def make_cookies(chrome_driver):
    cookies = {}
    try:
        chrome_driver.find_elements_by_xpath("//a")[1].click()
        for i in chrome_driver.get_cookies():
            cookies[i['name']] = i['value']
    except Exception:
        chrome_driver.close()
        get_cookies()
    if cookies == {}:
        chrome_driver.refresh()
        cookies = make_cookies(chrome_driver)
    print(cookies)
    return cookies


def daka(cookies):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')  # 改变标准输出的默认编码
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    response = requests.post(url=url, headers=headers, cookies=cookies, data=data)
    print(response.text)
    print(response.status_code)


def main():
    get_cookies()
    print("打卡成功")


if __name__ == '__main__':
    while (1):
        if time.localtime().tm_hour == 1:
            main()
        else:
            print("等待中……"+time.ctime())
        sleep(3400)
