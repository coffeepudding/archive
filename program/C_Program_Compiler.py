# coding:UTF-8

# 作成者 : 平野雅也

# 完成度はまだまだ低いです

# 初期設定
# 1.inputフォルダ内のtxtを変更する

# -----実行方法-----
# 0.Zドライブのどっかにsubprocess2のフォルダと一緒に置く
# 1.同階層以下にzipを置く
# 3.どっちもを利用しないときは，引数に0
# 4.入力ファイルを利用するときは，引数にr
# 5.出力ファイルを利用するときは，引数にw
# 6.どっちもを利用するときは，引数にa
# 7.「out_学生番号.txt」に出力される

import csv
import glob
import os
import re
import shutil
import subprocess2
from subprocess2 import PIPE
import sys
import time
import zipfile

# MACで動かすときはTrueに
DEBUG = False

# 出力ファイル対応
OUTPUT_FILE_NAME = ['out1.txt','out2.txt','out3.txt','out4.txt']

EXPATH = os.getcwd() + '/temp/'
ZIPPATH = './zip/'
TEMP = './temp/'
TEMPCONV = TEMP + 'conv.c'
PREFIX = 'enc_'
# 無限ループ発生時に書き出すメッセージ内容
INF_MESSAGE = '''プログラムが終了しませんでした
考えられる原因：無限ループ、終了条件の間違い
'''

# 無限ループを判定する猶予
TIMEOUT_SEC = 1

class Compiler:
    '''
    勉強兼ねてのクラス化
    理解できればそこそこ使える
    '''
    def initialize(self,i):
        '''
        インスタンスの初期化
        i:課題番号
        '''
        self.ex_num = i
        print('実行方法')
        self.execute_type()
        print('実行回数（実行結果例参考）')
        if DEBUG:
            self.trial = int(input())
        else:
            self.trial = int(raw_input())

    def initialize2(self,i,exe,num):
        '''
        インスタンスの初期化
        i:課題番号
        '''
        self.ex_num = i
        print('実行方法')
        self.execute_type(exe)
        print('実行回数（実行結果例参考）')
        self.trial = int(num)


    def execute_type(self,arg = ''):
        '''
        実行形式の指定
        キーボード入力と、出力ファイルについて保存する
        '''
        self.is_infile = False
        self.is_outfile = False
        self.is_pptx = False
        if len(arg) == 0:
            if DEBUG:
                argument = input()
            else:
                argument = raw_input()
        else:
            argument = arg

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
        elif argument == 'p':
            self.is_pptx = True
            print('パワーポイント')
        else:
            print('キーボード：なし\n出力ファイル：なし')


    def execute(self,argument):
        '''
        Popenの引数の指定
        argument:引数
        '''
        return subprocess2.Popen(argument, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)


    def output_code(self,cfile,fp):
        '''
        コードの内容をファイルに書き出す
        globしているのは、zipfile展開時にpathがおかしくなるため
        fp:書き込みファイル
        cfile:実行するcファイル名
        '''
        try:
            if DEBUG:
                convert = self.execute("nkf -w " + TEMP + cfile + ' > ' + TEMPCONV)
            else:
                convert = self.execute("./nkf32.exe -w " + TEMP + cfile + ' > ' + TEMPCONV)
            stdout, stderr = convert.communicate()
            code = open(TEMPCONV,'r')
            fp.write('exercise:' + str(self.ex_num+1) + '\r\n')
            fp.write('path:' + cfile + '\r\n')
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
        fp:出力ファイル
        '''
        fp.write('\r\n')
        fp.write('-------------------------------------------------\r\n')
        fp.write('\r\n\r\n')


    def compile_code(self,cStudent,cfile,fp):
        '''
        ソースコードをコンパイルする
        一応タイムアウトする
        cStudent:学生番号
        cfile:実行するコードのパス
        fp:出力ファイル
        '''
        print(u"コンパイル >> gcc -o " +
              cStudent + " " + TEMPCONV)
        result = self.execute("gcc -o " + cStudent + " " + TEMPCONV)
        stdout, stderr = result.communicate()
        os.remove(TEMPCONV)
        if isinstance(stderr,type(None)):
            return False
        check = stderr.decode('utf-8')
        if u'エラー' in check:
            print(u'コンパイルエラーです')
            fp.write('-----Compile Error!-----\r\n')
            fp.write(check.encode('utf-8'))
            return True
        elif 'error' in check:
            print(u'コンパイルエラーです')
            fp.write('-----Compile Error!-----\r\n')
            fp.write(check)
            return True
        return False


    def execute_program(self,num,fp):
        '''
        プログラムを実行し，ファイルに書き出す
        num:学生番号
        fp:出力ファイル
        '''
        print(u'実行 >> ' + str(num) + ".exe")
        fp.write('-----exercise' + str(self.ex_num+1) + '-----\r\n')
        fp.write('-----Execution result-----\r\n')
        for i in range(self.trial):
            fp.write('-----trial' + str(i+1) + '-----\r\n')
            if self.is_infile == True:
                if DEBUG:
                    result = self.execute('./' + num + ' < input/ex'+ \
                        str(self.ex_num+1)+'/trial'+str(i+1)+'.txt')
                else:
                    result = self.execute('./' + num + '.exe < input/ex'+ \
                        str(self.ex_num+1)+'/trial'+str(i+1)+'.txt')
            else:
                if DEBUG:
                    result = self.execute('./' + num)
                else:
                    result = self.execute('./' + num + '.exe')
            # 無限ループ対策
            if result.waitUpTo(TIMEOUT_SEC) == None:
                print(u'無限ループです')
                result.kill()
                # プロセス解放待ち
                time.sleep(1)
                fp.write(INF_MESSAGE)
            else:
                output, error = result.communicate()
                if DEBUG:
                    fp.write(output.decode('utf-8'))
                else:
                    fp.write(output)
                fp.write('\r\n')
                if self.is_outfile == True:
                    self.write_output(fp)
        try:
            if DEBUG:
                os.remove('./' + str(num))
            else:
                os.remove('./' + str(num) + ".exe")
        except:
            print('削除失敗しました')


    def write_output(self,fp):
        '''
        出力ファイルの内容をファイルに書き出す
        fp:出力ファイル
        '''
        try:
            print(u'出力ファイル名 >> ' + OUTPUT_FILE_NAME[self.ex_num])
            output = open(OUTPUT_FILE_NAME[self.ex_num], 'r')
            fp.write('Output File name : ' + OUTPUT_FILE_NAME[self.ex_num] + '\n')
            fp.write('-----output result-----\r\n')
            for line in output:
                fp.write(line)
            fp.write('\r\n')
            output.close()
            os.remove("./" + OUTPUT_FILE_NAME[self.ex_num])
            return True
        except:
            print('Output File Open Error!!')
            fp.write('Output File Open Error!!\r\n')
            return False


def ex_detect(fpath,cStudent):
    '''
    課題番号を検出
    ついでにpptxも展開している
    fpath:ファイルパス(ディレクトリパスも来る)
    cStudent:学生番号
    '''
    fname = os.path.split(fpath)[1]
    if len(fname) == 0:
        return -1
    matchOBJ = re.search('([0-9])\.(\w+)$', fpath)
    if isinstance(matchOBJ,type(None)):
        return -1
    basename = matchOBJ.group(1)
    ext = matchOBJ.group(2)
    if not fpath.startswith('_'):
        if re.match(ext,'c(pp)?') != None:
            tasknum = int(basename)
            return tasknum-1
        else:
            return -1


# def pptx():
#     ext == 'pptx':
#     zipdata.extract(fpath,path=EXPATH)
#     shutil.copy2(TEMP + fpath, "./output/" + cStudent + fname)
#     return -1


def main(args):
    '''
    メイン
    '''
    print('-----C Program Compiler ver.Ohara-----')
    print('キーボード入力なしの場合、0')
    print('キーボード入力ありの場合、r')
    print('出力ファイルありの場合、w')
    print('どっちもありの場合、w')
    print('pptxの場合、p')
    debug_input = []
    if os.path.isfile('debug.txt'):
        with open('debug.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                debug_input.append(row)
    # print('課題数')
    num_of_task = 4
    # num_of_task = input()
    # メソッド配列の作り方がイマイチわからない
    comp = []
    # メソッドの初期化
    for i in range(num_of_task):
        print('exercise ' + str(i+1))
        comp.append(Compiler())
        if len(debug_input) == num_of_task:
            comp[i].initialize2(i,debug_input[i][0],debug_input[i][1])
        else:
            comp[i].initialize(i)

    # ファイル探索
    zipdirlist = []
    for x in os.listdir(ZIPPATH):
        # zipファイルだけ取得
        if x.endswith('.zip'):
            # ファイルのパスをフルパスに変更
            zipdirlist.append(ZIPPATH + x)

    # zipを1つずつ処理
    for zipfiledir in zipdirlist:
        # 学生番号を取得する正規表現
        cStudent = re.search('[0-9]{8}', zipfiledir).group(0)
        # outputのフォルダ内にout_12345678.txtが出来る
        outfile = open('output/out_' + cStudent + '.txt','w')
        # zip内のファイルを1つずつ参照
        with zipfile.ZipFile(zipfiledir) as zipdata:
            for name in zipdata.namelist():
                # 課題番号判定ついでにpptxも展開
                ex_num = ex_detect(name,cStudent)
                # ソースコードじゃなかったら終了
                if ex_num == -1:
                    continue
                # ファイル展開
                zipdata.extract(name,path=EXPATH)
                # コードの内容をファイルに書き出す
                comp[ex_num].output_code(name,outfile)
                # 対象ソースコードをコンパイル
                # コンパイルに失敗したらTrue
                if comp[ex_num].compile_code(cStudent,EXPATH+name,outfile):
                    # 改行と改ページの挿入
                    comp[ex_num].insert_newpage(outfile)
                    continue
                # 対象プログラムを実行
                comp[ex_num].execute_program(cStudent,outfile)
                # 改行と改ページの挿入
                comp[ex_num].insert_newpage(outfile)
        outfile.close()
    print(u'終了!')


if __name__ == "__main__":
    main(sys.argv)
