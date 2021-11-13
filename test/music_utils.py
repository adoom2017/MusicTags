# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  python
@文件 :  music_utils.py
@时间 :  2021/11/06 00:29
@作者 :  will
@版本 :  1.0
@说明 :   音乐工具类，包含了修改标签和添加封面等方法

'''
import os

import music_tag
from mutagen.mp4 import MP4, MP4Cover


class MusicUtils(object):

    @staticmethod
    def music_add_cover(music_path, cover_path):
        """
    给音乐文件添加封面图片
        Args:
            music_path: 音乐文件的路径
            cover_path: 封面图片所在的路径
        """
        if os.path.isfile(music_path):
            if os.path.isfile(cover_path):
                video = MP4(music_path)
                with open(cover_path, "rb") as f:
                    video["covr"] = [
                        MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                    ]
                video.save()
            else:
                raise Exception("封面图片文件文件不存在！")
        else:
            raise Exception("音乐文件文件不存在！")
        pass

    @staticmethod
    def music_edit_tags(file_path, title, artist, album='', lyrics='', genre='Mandopop'):
        """
    编辑音乐文件的标签
        Args:
            file_path: 文件路径
            title: 歌曲名
            artist: 歌手
            album: 专辑
            genre: 类型
            year: 发行年份
        """
        if not album:
            album = title

        music = music_tag.load_file(file_path)
        music['title'] = title
        music['artist'] = artist
        music['album'] = album
        music['genre'] = genre
        music['lyrics'] = lyrics
        music.save()

    @staticmethod
    def music_print_tags(file_path):
        """
    打印音乐文件的标签信息
        Args:
            file_path:  音乐文件的所在路径
        """
        print("-------------------------------------------")
        music = music_tag.load_file(file_path)
        print("歌曲名：", music['title'])
        print("歌手：", music['artist'])
        print("专辑：", music['album'])
        print("类型：", music['genre'])
        print("-------------------------------------------")
        pass
