# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import os
import time
import urllib.request
import re
import getpass
import random
import platform
from os import path
import zipfile
from subprocess import run
import datetime

del_like_cnt = 0 # 统计删除微博数量

def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        zip_file.extract(names, path.dirname(__file__))
    zip_file.close()

def dl_driver():
    request = urllib.request.Request('http://npm.taobao.org/mirrors/chromedriver/')
    response = urllib.request.urlopen(request)
    html = response.read()
    pat = re.compile(r'/mirrors/chromedriver/(.+?)/')
    result = pat.findall(str(html))
    flag = 0
    # 获得版本数组
    # 想了想可以用xpath快速匹配的，但觉得安装第三方模块也需要时间
    version = get_version()
    chrome_version = version[0] + '.' + version[1] + '.' + version[2]

    for item in result:
        if chrome_version in item:
            flag = item
            break

    print("--------------正在下载驱动--------------")

    run("curl -O -L http://npm.taobao.org/mirrors/chromedriver/{0}/chromedriver_win32.zip".format(
        flag), shell=True)

    un_zip("chromedriver_win32.zip")
    print("--------------驱动下载成功--------------")

    print("--------------驱动解压成功--------------")

def time_count(func):
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()  # 程序开始时间
        func(*args, **kwargs)
        over_time = datetime.datetime.now()  # 程序结束时间
        total_time = (over_time - start_time).total_seconds()
        print('----------本程序共运行了%s秒----------' % total_time)
    return int_time

def get_version():
    cmd = 'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version'
    rw = os.popen(cmd, 'r', 1).read()
    version = re.sub(r'([^\d^\.]+)', '', rw).split(".")
    return version

def weibo_login(username, password):
    cur_path = os.getcwd() + '\\chromedriver'

    opts = ChromeOptions()
    opts.add_experimental_option("detach", True)

    driver = webdriver.Chrome(executable_path=cur_path, options=opts)
    driver.get("https://weibo.com")
    time.sleep(10)
    driver.find_element_by_id("loginname").send_keys(username)
    time.sleep(1)
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(3)
    driver.get("https://weibo.com")
    return driver

def load():
    # username = input("请输入账号：")
    # password = getpass.getpass("请输入密码:(密码将自动隐藏)")
    username="joyhooian@hotmail.com"
    password="j2K)gP@JHE>%cFzu\r\n"
    print("1.清理失效收藏微博请按1")
    print("2.清理失效转发微博请按2")
    # num = int(input(""))
    # page = input("\n请输入从第几页开始清除(直接按回车则默认从第一页开始):")0.

    num=1
    page=1

    if page == "" or page == "\n":
        page_num = 1
    else:
        page_num = int(page)

    return (username, password, num, page_num)
@time_count
def del_like(driver, count=1):
    global del_like_cnt
    page = 1
    url = "https://weibo.com/like/outbox?page="
    driver.get(url + str(page))
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    text_page = driver.find_element_by_class_name("W_scroll").find_element_by_tag_name("a").get_attribute("textContent")
    max_page = int(re.sub(r'([\D]+)', '', text_page))
    if max_page == 1:
        while 1:
            try:
                driver.find_element_by_class_name("delfav").click()
            except Exception as e:
                print(e)
                break
            else:
                continue
    else:
        while 1:
            try:
                driver.find_element_by_link_text("取消赞。").click()
            except Exception as e:
                print(e)
                error = str(e)
                message = error.split(":")
                if message[1] == " no such element":
                    page = page + 1
                    if page > max_page:
                        break
                    url = "https://weibo.com/like/outbox?page="
                    driver.get(url + str(page))
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(5)
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/10000)")
                    time.sleep(1)
                    
                    continue
                else:
                    continue
            else:
                continue
            


                



def main():
    opt = load()
    print("\n--------------一键清理正在启动--------------\n")
    username = opt[0]
    password = opt[1]
    count = opt[-1]

    # 如果没有驱动，自动下载
    if not os.path.exists(os.getcwd() + '/chromedriver_win32.zip'):
        dl_driver()
    driver = weibo_login(username, password)

    #Test Code Begin
    del_like(driver, count)
    #Test Code End

    # if opt[2] == 1:
    #     del_fav(driver, count)
    #     print("--------------已清除{0}条失效微博--------------\n".format(del_fav_count))
    # elif opt[2] == 2:
    #     del_repost(driver, count)
    #     print("--------------已清除{0}条失效微博--------------～\n".format(del_re_count))
    input("--------------请按回车结束本程序。感谢使用～--------------")
    driver.quit()

if __name__ == "__main__":
    main()