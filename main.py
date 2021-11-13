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

from MusicTag import MusicTag
from QQMuiscAPI import QQMuiscAPI
from Utils import get_dir_file_list, download, get_music_file_info

if __name__ == '__main__':
    music_path = input("请输入音乐文件所在的目录：")
    # 判断输入的目录是否存在
    if music_path and os.path.isdir(music_path):
        #     # 初始化
        qq = QQMuiscAPI()
        mt = MusicTag()
        # 遍历目录下的所有文件
        music_file_list = get_dir_file_list(music_path, exts=['.mp3','.m4a'])
        for music_file in music_file_list:
            # 从文件名中获取到歌手和音乐名称
            music_info = get_music_file_info(music_file['base_name'])
            print("------------------" + music_info['singer'] + "-" + music_info[
                'name'] + "--------------------------")
            # 获取歌曲信息
            print('开始匹配歌曲：' + music_file['base_name'])
            music = qq.get_music_info(music_info['name'] + ' ' + music_info['singer'])
            music['path'] = music_file.get('path')
            # 如果从QQ音乐获取失败
            if not music:
                print("Oops：从QQ音乐获取歌曲信息失败！！")
                music['title'] = music_info['name']
                music['artist'] = music_info['singer']
                music['album'] = music_info['name']
                music['genre'] = "Pop"
                music['lyrics'] = "暂时没有歌词"


            print("开始编辑标签:" + music_info['name'])
            mt.edit_tag(music)
            # 下载歌曲封面
            if music.get('cover'):
                print("开始下载专辑封面:" +  music['album'])
                cover_path = music_path + '/' + music_info['singer'] + "-" + music_info['name'] + ".jpg"
                download(music.get('cover', ""), cover_path)
                # 给歌曲添加封面
                print("开始添加专辑封面:" +  music['album'])
                if mt.add_cover(music.get('path', ""), cover_path):
                    print("专辑封面添加成功:" + music['album'])
                else:
                    print("Oops! 专辑封面添加失败啦！！！" )
            print("歌曲编辑完成:" + music_info['name'])
            print("------------------------------------------------------------")

        qq.close()
        exit()
    else:
        print("Oops： 你输入的目录不存哟！！！")
    #     # 初始化
    #     qq = QQMuiscAPI()
    #     mt = MusicTag()
    #
    #

    #     # 获取歌曲信息
    #     music = qq.get_music_info(music_name + ' ' + singer)
    #     # 如果获取失败
    #     if not music:
    #         print("歌曲信息获取失败！！！")
    #         music['title'] = music_name
    #         music['artist'] = singer
    #         music['album'] = music_name
    #         music['genre'] = "Pop"
    #         music['lyrics'] = "暂时没有歌词"
    #         # music['year'] = ""
    #
    #     music['path'] = file_path[i]
    #     mt.edit_tag(music)
    #     # 下载歌曲封面
    #     if music.get('cover'):
    #         print("开始下载歌曲封面......")
    #         cover_path = __MUSIC_PATH__ + '/' + singer + "-" + music_name + ".jpg"
    #         download(music.get('cover', ""), cover_path)
    #         # print("歌曲封面下载完成")
    #         # 给歌曲添加封面
    #         mt.add_cover(music.get('path', ""), cover_path)
    #     print("------------------------------------------------------------")
    #     qq.close()
    #
    # pass
