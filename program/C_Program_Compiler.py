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
import collections
import datetime
import glob
import os
import re
import shutil
import subprocess2
from subprocess2 import PIPE
import sys
import time
import traceback
import zipfile

# MACで動かすときはTrueに
DEBUG = True

if sys.version_info[0] == 3:
    PY3 = True
else:
    PY3 = False


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
        if PY3:
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
            if PY3:
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


    def output_code(self,cfile,fp,filetime):
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
            fp.write(filetime.strftime("タイムスタンプ:%c") + '\r\n')
            fp.write('-----code-----\r\n')
            for line in code:
                fp.write(line)
            fp.write('\r\n')
            code.close()
            print('出力完了')
        except:
            print('読み込み失敗')
            traceback.print_exc()
            fp.write('ファイル読み込み失敗\r\n')


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
        check = stderr.decode('utf-8')
        if u'エラー' in check:
            print(u'コンパイルエラーです')
            fp.write('-----コンパイルエラー!-----\r\n')
            fp.write(check.encode('utf-8'))
            return True
        elif 'error' in check:
            print(u'コンパイルエラーです')
            fp.write('-----コンパイルエラー!-----\r\n')
            fp.write(check)
            return True
        return False


    def execute_program(self,num,fp):
        '''
        プログラムを実行し，ファイルに書き出す
        引数
        num:学生番号
        fp:出力ファイル

        戻り値
        point:csvに出力する点数
        '''
        point = 0
        print(u'実行 >> ' + str(num) + ".exe")
        fp.write('-----課題' + str(self.ex_num+1) + '-----\r\n')
        fp.write('-----実行結果-----\r\n')
        for i in range(self.trial):
            fp.write('-----実行例' + str(i+1) + '-----\r\n')
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
                point = 3
            else:
                output, error = result.communicate()
                if DEBUG:
                    fp.write(output.decode('utf-8'))
                else:
                    fp.write(output)
                fp.write('\r\n')
                point = 4
                if self.is_outfile == True:
                    self.write_output(fp)
                point = 5
        try:
            if DEBUG:
                os.remove('./' + str(num))
            else:
                os.remove('./' + str(num) + ".exe")
        except:
            print('削除失敗しました')
            traceback.print_exc()

        return point


    def write_output(self,fp):
        '''
        出力ファイルの内容をファイルに書き出す
        fp:出力ファイル
        '''
        try:
            print(u'出力ファイル名 >> ' + OUTPUT_FILE_NAME[self.ex_num])
            output = open(OUTPUT_FILE_NAME[self.ex_num], 'r')
            fp.write('Output File name : ' + OUTPUT_FILE_NAME[self.ex_num] + '\n')
            fp.write('-----実行結果-----\r\n')
            for line in output:
                fp.write(line)
            fp.write('\r\n')
            output.close()
            os.remove("./" + OUTPUT_FILE_NAME[self.ex_num])
            return True
        except:
            print('出力ファイル読み込み失敗')
            traceback.print_exc()
            fp.write('出力ファイル読み込み失敗\r\n')
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
    matchOBJ = re.search('(ex)?[0-9]{1,2}_([0-9])\.(\w+)$', fname)
    if isinstance(matchOBJ,type(None)):
        return -1
    ex_check = matchOBJ.group(1)
    basename = matchOBJ.group(2)
    ext = matchOBJ.group(3)
    if not fpath.startswith('_'):
        if re.match(ext,'c(pp)?') != None or ext == 'pptx':
            if ex_check != 'ex':
                print('ソースファイル名に異常があります。')
                print('ソースファイル名:'+fname)
            tasknum = int(basename)
            return tasknum-1
        else:
            return -1


def main(args):
    '''
    メイン
    '''
    print('-----わたり自動化-----')
    print('キーボード入力なしの場合、0')
    print('キーボード入力ありの場合、r')
    print('出力ファイルありの場合、w')
    print('どっちもありの場合、w')
    print('pptxの場合、p')

    # 実行パターンが存在するならば、自動化する
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

    # 辞書初期化
    saiten_dict = collections.OrderedDict()
    # 順データが存在するならば、利用する
    if os.path.isfile('order.csv'):
        with open('order.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                for s_id in row:
                    if len(s_id) != 0:
                        saiten_dict[s_id] = {}

    # zipを1つずつ処理
    for zipfiledir in zipdirlist:
        # 学生番号を取得する正規表現
        cStudent = re.search('[0-9]{8}', zipfiledir).group(0)

        saiten = collections.defaultdict(int)
        saiten.update({'ex1':0,'ex2':0,'ex3':0,'ex4':0})
        saiten['s_id'] = cStudent
        verify = collections.defaultdict(int)
        # zip内のファイルを1つずつ参照
        # timestampの対策のため、コードを分割する
        with zipfile.ZipFile(zipfiledir) as zipdata:
            for name in zipdata.namelist():
                try:
                    # 課題番号判定ついでにpptxも展開
                    ex_num = ex_detect(name,cStudent)
                    # ソースコードじゃなかったら終了
                    if ex_num == -1:
                        continue
                    # ファイル展開
                    zipdata.extract(name,path=EXPATH)
                    # タイムスタンプを取得
                    zinfo = zipdata.getinfo(name)
                    d = zinfo.date_time
                    # datetime型に変換
                    zdate = datetime.datetime(d[0],d[1],d[2],d[3],d[4],d[5])
                    # 辞書に書きこんでおく
                    program_info = collections.defaultdict(int)
                    program_info['task'] = ex_num
                    program_info['filepath'] = name
                    program_info['timestamp'] = zdate
                    verify[str(ex_num)] = program_info
                    # pptxなら展開
                    if comp[ex_num].is_pptx == True:
                        shutil.copy2(TEMP + name, "./output/" + cStudent + fname)
                        continue
                except:
                    traceback.print_exc()
                    print('原因不明')

        # outputのフォルダ内にout_12345678.txtが出来る
        outfile = open('output/out_' + cStudent + '.txt','w')
        for i in range(len(verify)):
            try:
                outfile.write(verify[str(i)]['timestamp'].strftime("タイムスタンプ%c"))
                # 時間の判定
                if i != 0:
                    if verify[str(i-1)]['timestamp'] < verify[str(i)]['timestamp']:
                        outfile.write("時間は正常です\r\n")
                # コードの内容をファイルに書き出す
                comp[i].output_code(verify[str(i)]['filepath'],outfile,verify[str(i)]['timestamp'])
                # 対象ソースコードをコンパイル
                # コンパイルに失敗したらTrue
                if comp[i].compile_code(cStudent,EXPATH+verify[str(i)]['filepath'],outfile):
                    saiten['ex' + str(i+1)] = 2
                    # 改行と改ページの挿入
                    comp[i].insert_newpage(outfile)
                    continue
                # 対象プログラムを実行
                point = comp[i].execute_program(cStudent,outfile)
                # 改行と改ページの挿入
                comp[i].insert_newpage(outfile)
                # 辞書テスト
                saiten['ex' + str(i+1)] = point
            except:
                traceback.print_exc()
                print('ソースファイル名に異常があります')

        saiten_dict[cStudent] = saiten
        outfile.close()

    with open('watari.csv', 'w') as csvfile:
        fieldnames = ['s_id', 'ex1', 'ex2', 'ex3', 'ex4']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for w in saiten_dict.values():
            writer.writerow(w)
    print(u'終了!')


if __name__ == "__main__":
    main(sys.argv)
