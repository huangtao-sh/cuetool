
无损音乐分拆工具
====

简介
---

本软件用来将从网上下载的无损格式音乐按附带的cue文件分拆成flac格式，将在分拆后
的音乐文件中写入META数据。

使用说明
----
    usage: cuetool.py [-h] [-f FORMAT] [-d OUTPUT_DIR] [CueFile [CueFile ...]]

    无损音乐拆分软件

    positional arguments:
        CueFile               cue文件

    optional arguments:
        -h, --help            show this help message and exit
    -f FORMAT, --format FORMAT
        输出音乐格式
    -d OUTPUT_DIR, --directory OUTPUT_DIR
        输出目录    

支持格式
----
输入格式：wv,aiff,shn,flac,ape,ofr,wav,tta,als,tak,bonk,mkw等格式。


其中各种格式取决于系统中安装的音乐库。

Test
----
