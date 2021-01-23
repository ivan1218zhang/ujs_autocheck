# -*- coding: utf-8 -*-
from selenium.webdriver import Chrome
import requests
from time import sleep
from PIL import Image
import cv2 as cv
import pytesseract
import time

url = "http://yun.ujs.edu.cn/xxhgl/yqsb/grmrsb"
# 学号和密码
id=""
keywords=""
# 自行复制post的data数据 字典格式 浏览器F12查看post的请求
data = {

}


def recognize_text(image):
    # 边缘保留滤波 去噪
    blur = cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
    # 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # 识别
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    return text


def _get_cookies():
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
    chrome_driver.find_element_by_xpath("//input[@id='captchaResponse']").send_keys(text)
    chrome_driver.find_element_by_xpath("//button[@type='submit']").click()
    try:
        chrome_driver.find_elements_by_xpath("//a")[1].click()
        cookies = make_cookies(chrome_driver)
        chrome_driver.close()
        daka(cookies)
    except Exception:
        chrome_driver.close()
        _get_cookies()


def make_cookies(chrome_driver):
    cookies = {}
    while cookies=={}:
        sleep(1)
        for i in chrome_driver.get_cookies():
            cookies[i['name']] = i['value']
        chrome_driver.refresh()
    return cookies


def daka(cookies):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    response = requests.post(url=url, headers=headers, cookies=cookies, data=data)
    print(response.status_code)


def main():
    _get_cookies()
    print("打卡成功")


if __name__ == '__main__':
    while (1):
        if time.localtime().tm_hour == 1:
            main()
        else:
            print("等待中……"+time.ctime())
        sleep(3400)