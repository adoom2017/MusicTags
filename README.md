# MusicTags
> 这是一个对音乐文件标签编辑的程序，该程序会根据你的音乐文件名，自动从QQ音乐匹配歌曲的信息，并设置好所有的标签

  
## 运行环境

- 操作系统：Centos7 或Mac OS(已经测试)
- 安装Chrome并下载好chromedirver
- 安装好扩展库
## 安装
首先安装Google Chrome浏览器和Selenium扩展安装方法请参考：

[Centos7-安装Chrome无GUI运行selenium-chromedriver](https://pgw1315.github.io/2021/11/03/Centos7-安装Chrome无GUI运行selenium-chromedriver/)
### 安装扩展库
```bash 
pip3 install music-tag
pip3 install mutagen
pip3 install eyed3
```
## 使用

```bash 
# 输入你的音乐文件所在的位置
python3 main.py
```