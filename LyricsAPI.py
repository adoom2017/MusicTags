# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  python
@文件 :  LyricsAPI.py
@时间 :  2021/11/06 02:52
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import re
import time
from urllib.parse import urlencode, quote
import selenium
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from web_utils import WebUtils


class LyricsAPI(object):
    SEARCH_URL = 'https://www.8lrc.com/search/?key='

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
        self.browser = selenium.webdriver.Chrome(executable_path="./mac_chromedriver", chrome_options=chrome_options)
        pass

    def get_text_lyrics(self, music):
        url = self.SEARCH_URL + quote(music, 'utf-8')
        self.browser.get(url)
        time.sleep(2)
        # 得到搜索结果列表
        s_res = self.browser.find_element(By.CLASS_NAME, 'cicont')

        lyrics = s_res.text
        code = lyrics.find(music)
        if code >= 0:
            # 得到歌曲详情页
            m_home_link=self.browser.find_element(By.CLASS_NAME,'tGequ').get_attribute('href')
            self.browser.get(m_home_link)
            # 获取图片
            cover_url=self.browser.find_element(By.CLASS_NAME,'cover').get_attribute('style')
            for item in re.finditer(r"\"(.*)\"",cover_url):
                cover_url=item.groups()[0]
            WebUtils.download()
        else:
            raise Warning(music+'的歌词没有找到！！！')



    def close(self):
        self.browser.close()


if __name__ == '__main__':
    la = LyricsAPI()
    la.get_text_lyrics('一次就好')
    time.sleep(5)
    la.close()
