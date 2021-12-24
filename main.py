# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  MusicTags
@文件 :  main.py
@时间 :  2021/11/06 03:46
@作者 :  will
@版本 :  1.0
@说明 :   主文件，程序的入口

'''

import os.path
import logging
from logging import config
import yaml
import sys, getopt

from MusicTag import MusicTag
from QQMuiscAPI import QQMuiscAPI
from Utils import get_dir_file_list, download, get_music_file_info

#加载日志配置
with open("config.yaml", 'r', encoding="utf-8")as f:
    logging_yaml = yaml.load(stream=f, Loader=yaml.FullLoader)
    logging.config.dictConfig(config=logging_yaml)

class process:
    '''
    get music tags from QQ music.
    '''
    def __init__(self, music_path):
        self.path = music_path
        self.qq_api = QQMuiscAPI()
        self.mt = MusicTag()
        self.logger = logging.getLogger("musicTags")

    def editTag(self, file_info):

        # 分割文件名 %artist - %name
        music_info = get_music_file_info(file_info['base_name'])
        self.logger.info("Begin to process file: %s, artist: %s, file: %s.", file_info['base_name'], music_info['artist'], music_info['name'])

        # 获取歌曲信息
        music = self.qq_api.get_music_info(music_info['name'] + ' ' + music_info['artist'])

        # 如果从QQ音乐获取失败
        if not music:
            self.logger.error("Failed to get music %s info from QQ.", file_info['base_name'])
            music['title'] = music_info['name']
            music['artist'] = music_info['artist']
            music['album'] = music_info['name']
            music['genre'] = "Pop"
            music['lyrics'] = "暂时没有歌词"

        music['path'] = file_info.get('path')

        self.mt.edit_tag(music)

        # 下载歌曲封面
        if music.get('cover'):
            self.logger.info("Begin to download cover of album %s.", music['album'])
            cover_path = self.path + '/' + music_info['artist'] + "-" + music_info['name'] + ".jpg"
            download(music.get('cover', ""), cover_path)

            # 给歌曲添加封面
            self.logger.info("Begin to add cover to music tag of album %s.", music['album'])
            if mt.add_cover(music.get('path', ""), cover_path):
                self.logger.info("Add cover succeed of album %s.", music['album'])
            else:
                self.logger.error("Add cover failed of album %s.", music['album'])
        self.logger.info("End to process file: %s, artist: %s, file: %s.", file_info['base_name'], music_info['artist'], music_info['name'])

    # 遍历所有文件
    def raversePath(self):
        if not os.path.isdir(self.path):
            self.logger.error("Invalid path: %s.", self.path)
            return False
        
        music_file_list = get_dir_file_list(self.path, exts=['.mp3','.m4a'])
        for file_info in music_file_list:
           self.editTag(file_info)

        self.qq_api.close()

if __name__ == '__main__':
    musicPath = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:",["path="])
    except getopt.GetoptError:
        print(sys.argv[0] + " -p <music file path>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0] + " -p <music file path>")
            sys.exit()
        elif opt in ("-p", "--path"):
            musicPath = arg

    p = process(musicPath)
    p.raversePath()

