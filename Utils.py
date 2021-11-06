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


def traverse_dir_files(root_dir, ext=None, is_sorted=True):
    """
    列出文件夹中的文件, 深度遍历
    :param root_dir: 根目录
    :param ext: 后缀名
    :param is_sorted: 是否排序，耗时较长
    :return: [文件路径列表, 文件名称列表]
    """
    names_list = []
    paths_list = []
    for parent, _, fileNames in os.walk(root_dir):
        for name in fileNames:
            if name.startswith('.'):  # 去除隐藏文件
                continue
            if ext:  # 根据后缀名搜索
                if name.endswith(tuple(ext)):
                    names_list.append(name)
                    paths_list.append(os.path.join(parent, name))
            else:
                names_list.append(name)
                paths_list.append(os.path.join(parent, name))
    if not names_list:  # 文件夹为空
        return paths_list, names_list
    return paths_list, names_list


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
        except Exception as e:
            print(e)
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
