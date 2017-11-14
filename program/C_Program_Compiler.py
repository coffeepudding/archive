# coding:UTF-8

# 作成者 : 平野雅也

# 完成度はまだまだ低いです

# 初期設定
# 1.INPUT_FILE_NAMEにinputフォルダのコンソール入力を記述する
# 2.EXPATHに出力ディレクトリを記述する(My Documentsみたいに空白があると動きません)
# 3.OUTPUT_FILE_NAMEに出力ファイル名を入力する(未実装)

# -----実行方法-----
# 0.Zドライブのどっかにsubprocess2のフォルダと一緒に置く
# 1.同階層以下にzipを置く
# 3.どっちもを利用しないときは，引数に0
# 4.入力ファイルを利用するときは，引数にr
# 5.出力ファイルを利用するときは，引数にw
# 6.どっちもを利用するときは，引数にa
# 7.「out_学生番号.txt」に出力される

import glob
import os
import time
import subprocess2
from subprocess2 import PIPE
import zipfile
import re
import time
import os
import shutil

# 出力ファイル対応
OUTPUT_FILE_NAME = ['out1.txt','out2.txt','out3.txt','out4.txt']

EXPATH = os.getcwd() + '/temp/'
ZIPPATH = './zip/'
TEMP = './temp/'
TEMPCONV = TEMP + 'conv.c'

# 無限ループ発生時に書き出すメッセージ内容
INF_MESSAGE = '''プログラムが終了しませんでした
考えられる原因：無限ループ、終了条件の間違い
'''

# 無限ループを判定する猶予
TIMEOUT_SEC = 1

class Compiler:

    def initialize(self,i):
        self.ex_num = i
        print('実行方法')
        self.execute_type()
        print('実行回数（実行結果例参考）')
        self.trial = int(input())


    def execute_type(self):
        self.is_infile = False
        self.is_outfile = False
        '''
        実行形式の指定
        '''
        if argument == 'r':
            print('キーボード：あり\n出力ファイル：なし')
            self.is_infile = True
        elif argument == 'w':
            print('キーボード：なし\n出力ファイル：あり')
            self.is_outfile = True
        elif argument == 'a':
            print('キーボード：あり\n出力ファイル：あり')
            self.is_infile = True
            self.is_outfile = True
        else:
            print('キーボード：なし\n出力ファイル：なし')


    def output_code(self,fp,cfile):
        '''
        コードの内容をファイルに書き出す
        globしているのは、zipfile展開時にpathがおかしくなるため
        fp:書き込みファイル
        cfile:実行するcファイル名
        '''
        try:
            convert = subprocess2.Popen("./nkf32.exe -w " + cfile + ' > ' + TEMPCONV
                , shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = convert.communicate()
            code = open(TEMPCONV,'r')
            fp.write('exercise : ' + str(self.ex_num+1) + '\r\n')
            fp.write('-----code-----\r\n')
            for line in code:
                fp.write(line)
            fp.write('\r\n')
            code.close()
            print('Code output finish')
        except:
            print('File Open Error!!')
            fp.write('File Open Error!!\r\n')


    def insert_newpage(self,fp):
        '''
        見やすいように改行と改ページを挿入する
        '''
        fp.write('\r\n')
        fp.write('-------------------------------------------------\r\n')
        fp.write('\r\n\r\n')


    def compile_code(self,cStudent,cfile,fp):
        '''
        ソースコードをコンパイルする
        一応タイムアウトする
        '''
        print(u"コンパイル >> gcc -o " +
              cStudent + " " + cfile)
        result = subprocess2.Popen("gcc -o " + cStudent + " " + TEMPCONV
            , shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = result.communicate()
        check = stderr.decode('utf-8')
        os.remove(TEMPCONV)
        if u'エラー' in check:
            print(u'コンパイルエラーです')
            fp.write('-----Compile Error!-----\r\n')
            fp.write(check.encode('utf-8'))
            return True
        return False


    def execute_subprocess(self,num, infile = ''):
        '''
        Popenの引数の指定
        '''
        return subprocess2.Popen('./' + num + '.exe' + infile
                           , stdout=PIPE, stdin=PIPE, shell=True)


    def execute_program(self,num,fp):
        '''
        プログラムを実行し，ファイルに書き出す
        '''
        print(u'実行 >> ' + str(num) + ".exe")
        fp.write('-----exercise' + str(self.ex_num+1) + '-----\r\n')
        fp.write('-----Execution result-----\r\n')
        for i in range(self.trial):
            fp.write('-----trial' + str(i+1) + '-----\r\n')
            if self.is_infile == True:
                result = execute_subprocess(num
                    ,' < input/ex'+str(self.ex_num+1)+'/trial'+str(i+1)+'.txt')
            else:
                result = execute_subprocess(num)
            # 無限ループ対策
            if result.waitUpTo(TIMEOUT_SEC) == None:
                print(u'無限ループです')
                result.kill()
                # プロセス解放待ち
                time.sleep(1)
                fp.write(INF_MESSAGE)
            else:
                output, error = result.communicate()
                fp.write(output)
                fp.write('\r\n')
        os.remove('./' + str(num) + ".exe")


    def write_output(self,fp):
        '''
        出力ファイルの内容をファイルに書き出す
        '''
        try:
            print(u'出力ファイル名 >> ' + OUTPUT_FILE_NAME[self.ex_num])
            output = open(OUTPUT_FILE_NAME[self.ex_num], 'r')
            fp.write('Output File name : ' + OUTPUT_FILE_NAME[self.ex_num] + '\n')
            fp.write('-----output result-----\r\n')
            for line in output:
                fp.write(line)
            fp.write('\r\n')
            os.remove("./" + OUTPUT_FILE_NAME[self.ex_num])
            return True
        except:
            print('Output File Open Error!!')
            fp.write('Output File Open Error!!\r\n')
            return False


def ex_detect(fpath,cStudent):
    fname = os.path.split(fpath)[1]
    basename, ext = re.search('([0-9])\.(\w+)$', fpath)
    if not fpath.startswith('_'):
        if re.match(ext,'c(pp)?') != None:
            tasknum = int(basename)
            return tasknum-1
        elif ext == 'pptx':
            zipdata.extract(fpath,path=EXPATH)
            shutil.copy2(TEMP + fpath, "./output/" + cStudent + fname)
            return -1
        else:
            return -1


def main():
    '''
    メイン
    '''
    print('-----C Program Compiler ver.Ohara-----')
    print('キーボード入力なしの場合、0')
    print('キーボード入力ありの場合、r')
    print('出力ファイルありの場合、w')
    print('どっちもありの場合、w')

    # print('課題数')
    num_of_task = 4
    # num_of_task = input()

    # 初期化
    for i in range(num_of_task):
        print('exercise ' + str(i))
        comp[i] = Compiler()
        comp[i].initialize(i)

    # ファイル探索
    zipdirlist = []
    for x in os.listdir(ZIPPATH):
        if x.endswith('.zip'):
            # ファイルのパスをフルパスに変更
            zipdirlist.append(ZIPPATH + x)

    for zipfiledir in zipdirlist:
        cStudent = re.search('[0-9]{8}', zipfiledir).group(0)
        outfile = open('output/out_' + cStudent + '.txt','w')
        with zipfile.ZipFile(zipfiledir) as zipdata:
            for name in zipdata.namelist():
                # 課題番号判定
                # ついでにpptxも展開
                if (ex_num = ex_detect(fpath,cStudent)) == -1:
                    continue
                # ファイル展開
                zipdata.extract(name,path=EXPATH)
                # コードの内容をファイルに書き出す
                comp[ex_num].output_code(outfile,TEMP + name)
                # 対象ソースコードをコンパイル
                if comp[ex_num].compile_code(cStudent,EXPATH+name,outfile):
                    # 改行と改ページの挿入
                    insert_newpage(outfile)
                    continue
                # 対象プログラムを実行
                comp[ex_num].execute_program(cStudent,outfile)
                if comp[ex_num].is_outfile:
                    comp[ex_num].write_output(outfile)
                # 改行と改ページの挿入
                insert_newpage(outfile)
        outfile.close()
    print(u'終了!')


if __name__ == "__main__":
    main()
