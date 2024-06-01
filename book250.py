import requests
import os
import sys
import io
import re
import csv
from bs4 import BeautifulSoup
from alive_progress import alive_bar

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')  #改变标准输出的默认编码



def Get_PageInfo(url,start_page,is_print_log):
    url = url + str(start_page)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    headers = {
        'User-Agent': user_agent,
        }
    response = requests.get(url, headers=headers)  
    content = response.text
    #print(content)
    Soup = BeautifulSoup(content,'html.parser')

    book_name = Soup.find_all('div',attrs={'class' : 'pl2'})
    name_list = []
    loop_numbers1 = 0

    if(is_print_log):
        for name in book_name:
        #total always will be 25, one page only get 25 books
            n = ""
            for i in name.a.get_text():
                if not i == " " and not i == '\n':
                    n = n + i
            print("Add name in {l}: {n}".format(l = loop_numbers1, n = n))
            name_list.append(n)
            loop_numbers1+=1
    else:
        for name in book_name:
        #total always will be 25, one page only get 25 books
            n = ""
            for i in name.a.get_text():
                if not i == " " and not i == '\n':
                    n = n + i
            name_list.append(n)
            loop_numbers1+=1

    loop_numbers1 = 0
    info_list = []

    book_info = Soup.find_all('p',attrs={'class' : 'pl'})

    for item in book_info:
        total = item.get_text()
        #print(item)
        #[清] 曹雪芹 著 / 人民文学出版社 / 1996-12 / 59.70元 
        #[英] 阿·柯南道尔 / 丁钟华 等 / 群众出版社 / 1981-8 / 53.00元/68.00元
        #[英] 贡布里希 (Sir E.H.Gombrich) / 范景中 / 广西美术出版社 / 2008-04 / 280.00
        #少年儿童出版社 / 1962 / 30.00元

        temp_list = re.split(r'/', total)
        #print(temp_list)

        if len(temp_list) == 4:
            #author = author[:-1]
            #publishing_house = publishing_house[1:-1]
            #date = date[1:-1]
            #price = price[1:]
            temp_dict = {
                'author' : temp_list[0][:-1],
                'publishing-house' : temp_list[1][1:-1],
                'date' : temp_list[2][1:-1],
                'price' : temp_list[3][1:],
            }
            #print("{l}: {d}".format(l = loop_number1, d = temp_dict))
            info_list.append(temp_dict)
            loop_numbers1 +=1
        
        elif len(temp_list) == 3:
            temp_dict = {
                'author' : "",
                'publishing-house' : temp_list[0][:-1],
                'date' : temp_list[1][1:-1],
                'price' : temp_list[2][1:],
            }
            #print("{l}: {d}".format(l = loop_number1, d = temp_dict))
            info_list.append(temp_dict)
            loop_numbers1 +=1

        else:
            temp_dict = {
                'author' : temp_list[0][:-1],
                'translator' : temp_list[1][1:-1],
                'publishing-house' : temp_list[2][1:-1],
                'date' : temp_list[3][1:-1],
                'price' : temp_list[4][1:],
            }
            info_list.append(temp_dict)
            #print("{l}: {d}".format(l = loop_number1, d = temp_dict))
            loop_numbers1 +=1

    loop_numbers1 = 0
    #print(name_list)
    for item_dict in info_list:
        item_dict.setdefault("No.",int(start_page) + loop_numbers1 + 1)
        item_dict.setdefault("book_name", name_list[loop_numbers1])
        loop_numbers1 += 1

    if(is_print_log):
        for i in range(len(info_list)):
            print("{i}: {n}".format(i = i ,n = info_list[i]))
    
    return info_list

    response.close()

def show_bar(url):
    with alive_bar(10,title = "Get_PageInfo: ") as bar:
        for i in range(0,250,25):
            Get_PageInfo(url,str(i),False)
            print("Finish page {n}.".format(n = int((i+25)/25)))
            bar()

def main():
    url = "https://book.douban.com/top250?start="
    page_list = []
    start_page = 0
    end_page = 25
    for i in range(start_page,end_page,25):
        page_list.append(Get_PageInfo(url,str(i),False))
    #[[page1-dicts], [page2-dicts], [....], [.....], ....]
    print(page_list[0][0])
    print(page_list[0][24])


    




main()
