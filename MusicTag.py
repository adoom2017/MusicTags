# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  MusicTags
@文件 :  MusicTag.py
@时间 :  2021/11/06 10:08
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import os

import eyed3
import music_tag
from eyed3.id3.frames import ImageFrame
from mutagen.mp4 import MP4, MP4Cover


class MusicTag(object):

    def __init__(self):
        pass

    def edit_tag(self, music):
        print("开始编辑" + music['path'] + "的标签......")
        music_file = music_tag.load_file(music['path'])
        music_file['title'] = music.get('title', "")
        music_file['artist'] = music.get('artist', "")
        music_file['album'] = music.get('album', "")
        music_file['genre'] = music.get('genre', "")
        music_file['lyrics'] = music.get('lyrics', "")
        # music_file['year'] = music['year']
        # print(music_file)
        music_file.save()
        # print("音乐文件的标签修改完成")

    def add_cover(self, music_path, cover_path):
        """
    给音乐文件添加封面图片
        Args:
            music_path: 音乐文件的路径
            cover_path: 封面图片所在的路径
        """
        print("开始给" + music_path + "添加封面图片......")
        if os.path.isfile(music_path):
            if os.path.isfile(cover_path):
                if music_path[-3:] == "m4a":
                    # m4a格式文件
                    video = MP4(music_path)
                    with open(cover_path, "rb") as f:
                        video["covr"] = [
                            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                        ]
                    video.save()
                elif music_path[-3:] == "mp3":
                    # mp3文件格式
                    file = eyed3.load(music_path)
                    if file.tag == None:
                        file.initTag()
                    file.tag.images.set(ImageFrame.FRONT_COVER, open(cover_path, 'rb').read(), 'image/jpeg')
                    file.tag.save()
                else:
                    pass
                os.remove(cover_path)

            else:
                print(cover_path + "封面图片文件文件不存在！")
        else:
            print(music_path + "音乐文件文件不存在！")
        print(music_path + "封面图片添加完成")
        pass
