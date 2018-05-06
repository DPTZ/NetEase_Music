#这次的任务很失败，走了好多的弯路，最后一个url解决了我所有的问题。。。
#高呼三声 百度google大法好，开源万岁！

import selenium
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import RequestException
import time
import os
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

song_id=[]
song_name=[]
song_url=[]
singer_name=[]



def get_song_id(name):
    name_url = 'http://music.163.com/#/search/m/?s=' + str(name) + '&type=1'
    driver.get(name_url)
    driver.switch_to_frame('g_iframe')
    # soup=BeautifulSoup(driver.page_source,'lxml')
    message=re.compile(r'<div class="text"><a href="(.*?)"><b title="(.*?)">.*?data-res-id="(.*?)".*?<div class="text"><a href=".*?">(.*?)</a>',re.S)
    items=re.findall(message,driver.page_source)
    count=1
    for item in items:
        print(count,'.'+'歌曲名称:',item[1],'歌手:',item[3])
        count+=1
        song_url.append(item[0])
        song_name.append(item[1])
        song_id.append(item[2])
        singer_name.append(item[3])
    return items

def panduan(items):
    print('-------------------------------------------------------------------')
    while(True):
        number=input('***请输入你想要下载歌曲的序号***\n')
        if number.isdigit() and int(number)<=int(len(items)):
            print(number)
            break
        else:
            print('#####请输入正确的序号#####')
    print('你想下载的歌曲是:',items[int(number)-1][1],'---',items[int(number)-1][3])
    return  items[int(number)-1][1],items[int(number)-1][2]



def get_song(song_id):
    song_url= 'http://music.163.com/song/media/outer/url?id={0}.mp3'.format(song_id)
    try:
        r=requests.get(song_url)
        if r.status_code==200:
            r.raise_for_status()
            return r.content
        return None
    except RequestException:
        return None


def save_song(name,content):
    try:
        with open('{0}.mp3'.format(name),'wb') as f:
            f.write(content)
            f.close()
        print(' ^-^ 下载成功，请在 {0} 中查看'.format(os.getcwd()))
    except:
        print('下载失败，请重试！！！')


def programmer_star():
    print('--------------------------NetEase Music----------------------------')
    print('                     TIME:{0}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
    print('---------------------------------DP--------------------------------')

def main():
    programmer_star()
    name=input('~~~请输入你想获取的音乐名称,按enter确认~~~\n')
    items=get_song_id(name)
    name,id=panduan(items)
    content=get_song(id)
    save_song(name,content)






if __name__=='__main__':
    main()
