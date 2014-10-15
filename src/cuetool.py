#!/usr/bin/python3
# 项目：无损音乐分拆工具
# 作者：黄涛
# 创建：2014－10－15

import os
from stdlib import read_file,write_file,read_shell,write_shell,\
     exec_shell

# 本程序支持的音频格式
FORMAT=['wav','aiff','shn','flac','ape','ofr','wv',
        'tta','als','tak','bonk','mkw']
# 输入文件的支持的扩展名
EXT=['wav','aiff','shn','flac','ape','ofr','wv','tta'
        'als','tak','bonk','mkw']

# 获取专辑名称的命令行
ALBUM_CMD='cueprint -d%%T "%s"'
# 生成TAG的命令行
CUETAG_CMD='cuetag "%s" "%s"/*.%s'
# 分拆音频文件的命令行
SHNSPLIT_CMD='shnsplit -o %s -t %%n-%%t -f "%s" -d "%s" "%s"'
# 生成文件夹的命令
MKDIR_CMD= 'mkdir "%s"'

class CueTool:
    def __init__(self):
        # 设置初始的输出路径、格式、CUE文件等内容
        self.output_dir=os.path.expanduser('~/音乐/Album')
        self.format='flac'
        self.cue_files=[]

    def get_dir(self,cuefile):
        # 生成输出目录，在原设置路径的基础加上专辑的名称
        album=read_shell(ALBUM_CMD%(cuefile))
        if not album:
            raise Exception('读取CUEFILE失败')
        album=album[0]
        d=os.path.join(self.output_dir,album)
        if os.path.isdir(d):
            # 如获目标路径存在，则重新生成
            i=1
            while True:
                t='%s(%d)'%(d,i)
                if os.path.isdir(t):
                    i+=1
                else:
                    d=t
                    break
        return d
        
    def proc(self):
        # 对输入的文件逐个执行
        for cue_file in self.cue_files:
            # 判断CUE文件是否存在
            if os.path.isfile(cue_file):
                d,e=os.path.splitext(cue_file)
                # 判断音乐文件是否存在
                for ext in EXT:
                    in_file=d+'.'+ext
                    if os.path.isfile(in_file):
                        self.split(in_file,cue_file)
                        break
                else:
                    raise Exception('同名音乐文件不存在')
            else:
                raise Exception('文件%s 不存在'%(cue_file))

    def split(self,in_file,cue_file):
        #将CUE_FILE转换成UTF8编码
        write_file(cue_file,read_file(cue_file))
        # 获取输出目录
        d=self.get_dir(cue_file)
        # 生成命令行
        cmds=[
            MKDIR_CMD%(d),
            SHNSPLIT_CMD%(self.format,cue_file,d,in_file),
            CUETAG_CMD%(cue_file,d,self.format),
            ]
        # 逐条执行命令
        [exec_shell(x) for x in cmds]

    @classmethod
    def run(cls):
        # 生成参数适配
        from argparse import ArgumentParser
        import sys
        parser=ArgumentParser(
                description='无损音乐拆分软件')
        parser.add_argument('-f','--format',
                action='store',
                help='输出音乐格式')
        parser.add_argument('-d','--directory',
                action='store',
                dest='output_dir',
                help='输出目录')
        parser.add_argument('cue_files',
                action='store',nargs='*',
                metavar='CueFile',
                help='cue文件')

        if len(sys.argv)==1:
            # 如未输入参数，则打印帮助内容
            parser.print_help()
        else:
            parser.parse_args(sys.argv[1:],cls()).proc() 
    
if __name__=='__main__':
    CueTool.run()
