# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  MusicTags
@文件 :  Utils.py
@时间 :  2021/11/06 05:49
@作者 :  will
@版本 :  1.0
@说明 :   

'''
import os
import time
import selenium


def get_music_file_info(music_name):
    name_split = music_name.split("-")
    singer = ''
    name = ''
    if len(name_split) == 2:
        singer = name_split[0]
        name = name_split[1]
    else:
        name = name_split[0]
    return {'name': name, 'singer': singer}


def get_dir_file_list(root_dir, exts=[]):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param exts: 后缀名列表
    :return: 文件信息字典
    """

    file_list = []
    for parent, _, file_name_list in os.walk(root_dir):
        for file_item in file_name_list:
            file = {}
            file_path = parent + "/" + file_item
            # 文件路径
            file['path'] = file_path
            # 文件名带后缀
            file['name'] = file_item
            # 文件名不带后缀
            file['base_name'] = os.path.splitext(file_item)[0]
            # 文件后缀
            file['suffix'] = os.path.splitext(file_item)[-1]
            # 所在目录
            file['parent'] = parent
            # 文件大小
            file['size'] = os.path.getsize(file_path)
            # print(file)
            # 如果后缀列表为空则全部添加，否则只返回后缀列表中的类型
            if exts:
                for ext in exts:
                    if ext == file['suffix']:
                        file_list.append(file)
            else:
                file_list.append(file)

    return file_list


def download(url, path):
    """
下载文件
    :param url: 文件链接
    :param path: 本地保存地址
    """
    import requests
    f = None
    if url and path:
        try:
            f = open(path, 'wb')
            response = requests.get(url)
            f.write(response.content)
            f.close()
            return True
        except Exception as e:
            print(e)
            return False
            pass
        finally:
            f.close()


def get_long_shot_image(driver, pic_name):
    """
    #设置chrome开启的模式，headless就是无界面模式
    # 创建一个参数对象，用来控制chrome以无界面模式打开
    :param driver:             浏览器对象
    :param pic_name:        需要保存的文件名或路径＋文件名
    :return:
    """
    # 打开网页

    # 加延时 防止未加载完就截图
    time.sleep(1)
    # 用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # 获取页面宽度及其宽度
    print(width, height)
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)
    time.sleep(1)
    # 截图并关掉浏览器
    driver.get_screenshot_as_file(pic_name)
    # driver.quit()
