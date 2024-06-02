import requests
import os
import sys
import io
import re
import csv
from bs4 import BeautifulSoup
from alive_progress import alive_bar

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')  #改变标准输出的默认编码


def FastGetComment(url):
    requests.packages.urllib3.disable_warnings()
    requests.Session().keep_alive = False
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    headers = {
        'User-Agent': user_agent,
        }
    url = url
    try:
        response = requests.get(url, headers=headers)
        content = response.text
        Soup = BeautifulSoup(content,'html.parser')
        items = Soup.find_all('div',attrs={'class' : 'short-content'})
        o_words = items[0].get_text()
        words = re.findall( r'\S*[^\s]', o_words)
        words = words[:-1]
        word = ""
        for temp in words:
            word = word+temp
        #print(word)
        response.close()
        return word
    except:
        print("Conntect WRONG!!!:{i} ".format(i = url))




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
    book_score = Soup.find_all('span',attrs={'class' : 'rating_nums'})
    name_list = []
    score_list = []
    url_list = []
    comment_list = []
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
            url_list.append(name.a['href'])
            loop_numbers1+=1
    else:
        for name in book_name:
        #total always will be 25, one page only get 25 books
            n = ""
            for i in name.a.get_text():
                if not i == " " and not i == '\n':
                    n = n + i
            name_list.append(n)
            url_list.append(name.a['href'])
            loop_numbers1+=1

    for score in book_score:
        score = float(score.get_text())
        score_list.append(score)
    
    for url in url_list:
        comment_list.append(FastGetComment(url))

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
                'translator' : None,
                'publishing-house' : temp_list[1][1:-1],
                'date' : temp_list[2][1:-1],
                'price' : temp_list[3][1:],
            }
            """
            price = 'CNY 78.00'
            \d+匹配1次或者多次数字，注意这里不要写成*，因为即便是小数，小数点之前也得有一个数字；
            \.?这个是匹配小数点的，可能有，也可能没有；
            \d*这个是匹配小数点之后的数字的，所以是0个或者多个
            """
            temp_dict['price'] =  re.findall(r"\d+\.?\d*",temp_dict['price'])[0]
            temp_dict['price'] = float(temp_dict['price'])
            temp_dict['date'] = temp_dict['date'][0:4]
            #print("{l}: {d}".format(l = loop_number1, d = temp_dict))
            info_list.append(temp_dict)
            loop_numbers1 +=1
        
        elif len(temp_list) == 3:
            temp_dict = {
                'author' : None,
                'translator' : None,
                'publishing-house' : temp_list[0][:-1],
                'date' : temp_list[1][1:-1],
                'price' : temp_list[2][1:],
            }
            temp_dict['price'] =  re.findall(r"\d+\.?\d*",temp_dict['price'])[0]
            temp_dict['price'] = float(temp_dict['price'])
            temp_dict['date'] = temp_dict['date'][0:4]
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
            temp_dict['price'] =  re.findall(r"\d+\.?\d*",temp_dict['price'])[0]
            temp_dict['price'] = float(temp_dict['price'])
            temp_dict['date'] = temp_dict['date'][0:4]
            info_list.append(temp_dict)
            #print("{l}: {d}".format(l = loop_number1, d = temp_dict))
            loop_numbers1 +=1

    loop_numbers1 = 0
    #print(name_list)
    for item_dict in info_list:
        item_dict.setdefault("No.",int(start_page) + loop_numbers1 + 1)
        item_dict.setdefault("book_name", name_list[loop_numbers1])
        item_dict.setdefault("score",score_list[loop_numbers1])
        item_dict.setdefault("url",url_list[loop_numbers1])
        item_dict.setdefault("comment",comment_list[loop_numbers1])
        loop_numbers1 += 1

    if(is_print_log):
        for i in range(len(info_list)):
            print("{i}: {n}".format(i = i ,n = info_list[i]))
    response.close()
    return info_list



def Csv_Save(data_list):
    file_path = r'E:\Anacondaa\CodeDataSave\douban-book\csv-data\Top250_book_data.csv'
    directory = os.path.dirname(file_path)
    if( not os.path.exists(directory)):
        os.makedirs(directory)
    
    header = ['No.','book_name','author','publishing-house','date','price','score','url','comment']
    data = []
    for pages_item in data_list:
        for pages_info in pages_item:
            data.append([int(pages_info['No.']),
                         pages_info['book_name'],
                         pages_info['author'],
                         pages_info['publishing-house'],
                         pages_info['date'],
                         pages_info['price'],
                         pages_info['score'],
                         pages_info['url'],
                         pages_info['comment']
                         ]
                         )

    with open(file_path,"w",encoding="utf-8", newline='') as file: #打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

def Analysis_CsvData():
    print("")


def show_bar(url):
    with alive_bar(10,title = "Get_PageInfo: ") as bar:
        for i in range(0,250,25):
            Get_PageInfo(url,str(i),False)
            print("Finish page {n}.".format(n = int((i+25)/25)))
            bar()


def main():
    url = "https://book.douban.com/top250?start="
    data_list = []
    start_page = 0
    end_page = 250
    for i in range(start_page,end_page,25):
        data_list.append(Get_PageInfo(url,str(i),False))
    #[[page1-dicts], [page2-dicts], [....], [.....], ....]
    #page_list[0][0]
    #{'author': '[清] 曹雪芹 著', 'publishing-house': '人民文学出版社', 'date': '1996-12', 'price': '59.70元', 'No.': 1, 'book_name': '红楼梦'}
    print(data_list[0][0])
    Csv_Save(data_list)


main()
