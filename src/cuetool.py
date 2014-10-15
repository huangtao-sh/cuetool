#!/usr/bin/python3
import os
from stdlib import read_file,write_file

FORMAT=['wav','aiff','shn','flac','ape','ofr','wv',
        'tta','als','tak','bonk','mkw']

EXT=['wav','aiff','shn','flac','ape','ofr','wv','tta'
        'als','tak','bonk','mkw']

ALBUM_CMD='cueprint -d%%T "%s"'

CUETAG_CMD='cuetag "%s" "%s"/*.%s'

SHNSPLIT_CMD='shnsplit -o %s -t %%n-%%t -f "%s" -d "%s" "%s"'

MKDIR_CMD= 'mkdir "%s"'

def read_shell(cmd):
    return os.popen(cmd).read().splitlines()

def write_shell(cmd,lines):
    with os.popen(cmd,'w') as fn:
        if isinstance(lines,str):
            fn.write(lines)
        elif type(lines)in(tuple,list):
            [fn.write('%s\n'%(x))for x in lines]

def exec_shell(cmd):
    os.system(cmd)

class CueTool:
    def __init__(self):
        self.output_dir=os.path.expanduser('~/音乐/Album')
        self.format='flac'
        self.cue_files=[]

    def get_dir(self,cuefile):
        album=read_shell(ALBUM_CMD%(cuefile))
        if not album:
            raise Exception('读取CUEFILE失败')
        album=album[0]
        d=os.path.join(self.output_dir,album)
        if os.path.isdir(d):
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
        for cue_file in self.cue_files:
            if os.path.isfile(cue_file):
                d,e=os.path.splitext(cue_file)
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
        d=self.get_dir(cue_file)
        cmds=[
            MKDIR_CMD%(d),
            SHNSPLIT_CMD%(self.format,cue_file,d,in_file),
            CUETAG_CMD%(cue_file,d,self.format),
            ]
        [exec_shell(x) for x in cmds]

    @classmethod
    def run(cls):
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
            parser.print_help()
        else:
            parser.parse_args(sys.argv[1:],cls()).proc() 
    
if __name__=='__main__':
    CueTool.run()
