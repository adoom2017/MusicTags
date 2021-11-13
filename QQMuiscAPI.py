# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  MusicTags
@文件 :  QQMuiscAPI.py
@时间 :  2021/11/06 04:16
@作者 :  will
@版本 :  1.0
@说明 :   从QQ音乐获取歌曲信息

'''
import os
import time
import platform
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Config import Config
from Utils import download


class QQMuiscAPI(object):
    def init_env(self):
        """
初始化运行环境
        """

        # 初始化驱动
        sysstr = platform.system()
        if sysstr == "Linux":
            # print("当前使用的是Linux系统")
            Config.CHROME_DIRVER_PATH += '/chromedriver'
            Config.SYSTEM_IS_LINUX = True
        else:
            # print("当前使用的是其他系统")
            Config.CHROME_DIRVER_PATH += '/mac_chromedriver'
            Config.SYSTEM_IS_LINUX = False
        pass

    def init_dirver(self):
        """
初始化驱动所有设置
        """
        self.chrome_options = Options()
        # 设置浏览器是否无头运行，如果是Linux系统则默认无头运行，如果是其他系统，则根据CHROME_NO_HEAD的值决定是否无头运行呢
        if Config.SYSTEM_IS_LINUX:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument('--disable-gpu')
            self.chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
            Config.CHROME_IS_RUN_NO_HEAD = True
        else:
            if Config.CHROME_NO_HEAD:
                self.chrome_options.add_argument("--headless")
                self.chrome_options.add_argument('--disable-gpu')
                self.chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
                Config.CHROME_IS_RUN_NO_HEAD = True
        # 屏蔽无头浏览器特征
        self.chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

        self.driver = webdriver.Chrome(executable_path=Config.CHROME_DIRVER_PATH, chrome_options=self.chrome_options)
        self.driver.maximize_window()
        # 屏蔽无头浏览器特征
        with open('libs/stealth.min.js') as f:
            js = f.read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        # 隐式等待
        self.driver.implicitly_wait(20)

    def __init__(self):
        self.driver = None
        self.init_env()
        self.init_dirver()

    def get_music_info(self, keywd):
        music = {}
        try:
            # 打开搜索页面
            search_url = 'https://y.qq.com/n/ryqq/search?w=' + keywd
            self.driver.get(search_url)
            # time.sleep(5)
            # 得到搜索结果的列表
            song_items = self.driver.find_elements(By.CLASS_NAME, 'songlist__songname_txt')
            if len(song_items) == 0:
                print('没有搜索到歌曲！！')
                return music
            # 得到歌曲详情页地址
            # print(song_items[0].find_element(By.TAG_NAME, 'a').get_attribute('href'))
            song_details_page_link = song_items[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
            print("QQ音乐详情页地址：" + song_details_page_link)

            self.driver.get(song_details_page_link)
            # 封装歌曲信息
            # 获取到歌曲名
            music['title'] = self.driver.find_element(By.CLASS_NAME, 'data__name_txt').text
            # 获取到歌手的名字
            music['artist'] = self.driver.find_element(By.CLASS_NAME, 'data__singer_txt').text
            # 获取到专辑名字
            data_info = self.driver.find_elements(By.CLASS_NAME, 'data_info__item_song')

            music['album'] = data_info[0].text.replace("专辑：", "")
            # 获取专辑的流派
            genre = data_info[2].text
            if genre.find("流派") >= 0:
                music['genre'] = genre.replace("流派：", "")
            else:
                music['genre'] = "Other"

            # 获取到歌词
            # 点击展开
            more_but = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div[1]/div[2]/a')
            self.driver.execute_script("arguments[0].scrollIntoView();", more_but)
            time.sleep(1)
            more_but.click()
            time.sleep(1)
            lyrics = self.driver.find_element(By.ID, 'lrc_content')
            music['lyrics'] = lyrics.text

            # 获取专辑封面
            music['cover'] = self.driver.find_element(By.CLASS_NAME, 'data__photo').get_attribute('src')
            # print(music)
        except Exception as e:
            print(e)
            pass
        return music

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    qq = QQMuiscAPI()
    music = qq.get_music_info('漂洋过海来看你')
    download(music['cover'], "covers/pp.jpg")
    # print(music)
    # music = qq.get_music_info('一次就好')
    # print(music)
    # time.sleep(10)
    qq.close()
