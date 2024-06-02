import os
import io
import csv
import sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re
import requests
import threading
import concurrent.futures
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')  #改变标准输出的默认编码


def GetText(url):
    requests.packages.urllib3.disable_warnings()
    requests.Session().keep_alive = False
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    headers = {
        'User-Agent': user_agent,
        }
    response = requests.get(url, headers=headers)  
    content = response.text
    Soup = BeautifulSoup(content,'html.parser')
    items = Soup.find_all('div',attrs={'class' : 'short-content'})
    i = items[0]
    words = re.findall( r'\S*[^\s]', i.get_text())
    words = words[:-1]
    word = ""
    for temp in words:  
        word = word+temp
    response.close()
    return word

def GetList(url):
    requests.packages.urllib3.disable_warnings()
    requests.Session().keep_alive = False
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    headers = {
        'User-Agent': user_agent,
        }
    response = requests.get(url, headers=headers)  
    content = response.text
    Soup = BeautifulSoup(content,'html.parser')
    items = Soup.find_all('div',attrs={'class' : 'pl2'})
    url_list = []
    for item in items:
        url_list.append(item.a['href'])
    response.close()
    return url_list


def t1(k1,k2):
    return  (k1 + k2)

def useCThreading1(numbers,func,keywords):
    result_list = []
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交任务给线程池
        for i in range(numbers):
            future = executor.submit(func,keywords[i])
            # future = executor.submit(lambda temp_func:func(*temp_func),dict or (1,2) or [1,2,3] is ok too)
            # 等待任务完成，并获取返回值
            result = future.result()
            result_list.append(result)
    return result_list

def useCThreading2(loop1,loop2,func,keywords):
    result_list = []
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交任务给线程池
        for i in range(loop1):
            for j in range(loop2):
                future = executor.submit(func,keywords[i][j])
                # future = executor.submit(lambda temp_func:func(*temp_func),dict or (1,2) or [1,2,3] is ok too)
                # 等待任务完成，并获取返回值
                result = future.result()
                result_list.append(result)
    return result_list



def main():
    url = "https://book.douban.com/top250?start="
    o_url_list = []
    for i in range(0,250,25):
        o_url_list.append(url+str(i))
    print(len(o_url_list))
    url_list = useCThreading1(len(o_url_list),GetList,o_url_list)
    result = useCThreading2(len(url_list),len(url_list[0]),GetText,url_list)
    print(result[:10])



main()




    