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
# 音乐文件所在的目录
__MUSIC_PATH__ = "/Users/will/Code/MusicTags/music"

# __MUSIC_PATH__ = "/Users/will/Code/MusicTags/music/李荣浩-老街.mp3"

from pathlib import Path

from MusicTag import MusicTag
from QQMuiscAPI import QQMuiscAPI
from Utils import traverse_dir_files, download

if __name__ == '__main__':
    # 遍历目录下的所有文件
    file_path, file_name = traverse_dir_files(__MUSIC_PATH__, ext='mp3')
    for i, file in enumerate(file_name):
        # 初始化
        qq = QQMuiscAPI()
        mt = MusicTag()

        file_name = file.split('.')[0]
        file_name = file_name.split('-')
        # 获取到歌手和歌名
        if len(file_name) > 1:
            singer = file_name[0]
            music_name = file_name[1]
        else:
            singer = ""
            music_name = file_name[0]

        print("----------------------" + music_name + "------------------------------")
        # 获取歌曲信息
        music = qq.get_music_info(music_name + ' ' + singer)
        # 如果获取失败
        if not music:
            print("歌曲信息获取失败！！！")
            music['title'] = music_name
            music['artist'] = singer
            music['album'] = music_name
            music['genre'] = "Pop"
            music['lyrics'] = "暂时没有歌词"
            # music['year'] = ""

        music['path'] = file_path[i]
        mt.edit_tag(music)
        # 下载歌曲封面
        print("开始下载歌曲封面......")
        cover_path = __MUSIC_PATH__ + '/' + singer + "-" + music_name + ".jpg"
        download(music.get('cover', ""), cover_path)
        # print("歌曲封面下载完成")
        # 给歌曲添加封面
        mt.add_cover(music.get('path', ""), cover_path)
        # print(music)
        print("------------------------------------------------------------")
        qq.close()

    pass
