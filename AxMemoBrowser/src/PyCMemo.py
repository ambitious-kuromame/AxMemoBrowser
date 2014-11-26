#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2014/11/26

@author: aceax00
'''

#必要モジュールのインポート
import os;
import sys;
import re;
import codecs;


class PyCMemo:
    def __init__(self,root_dir=''):
        #クラスメンバの初期化
        print('[PyCMemo.__init__]');
        self.pwd = '';                  #検索時のrootディレクトリ
        self.file_list = [];            #検索したファイル一覧
        self.pattern = [];              #検索ワード(正規表現可能)．リスト形式で最後尾が最新の検索ワード．
        self.isRead = 0;                #一度でも検索したかの確認用フラグ
        #カレントディレクトリ or 指定ディレクトリを指定する
        if root_dir != '':              
            self.pwd = root_dir;
        else:
            self.pwd = '';                  

    def ReadDir(self):
        #変数の初期化
        print('[PyCMemo.ReadDir]');
        if self.pwd == '':
            self.pwd = os.path.abspath(os.path.dirname(__file__));
        print(self.pwd);
        #カレントディレクト以下を探索．
        #トップダウンで検索する．
        for root, dirs, files in os.walk(self.pwd):
            for file_ in files:
                full_path = os.path.join(root, file_);
                self.file_list.append(full_path);
                print(full_path);
        #検索結果をソート
        self.file_list.sort();
        #print(self.file_list);
                
    def SearchString(self,pattern):
        #変数の初期化
        print('[PyCMemo.SearchString]');
        self.pattern.append(pattern);
        #正規表現の検索エンジンの初期化
        ptn = re.compile(self.pattern[-1]);
        #一度でもファイルを読んでいない場合はReadDirを呼び出す
        if self.isRead == 0: self.ReadDir(),
        self.isRead = 1;
        #再帰的にファイルを探索
        for fname in self.file_list:
            print('=検索開始=');
            print(fname);
            with codecs.open(fname,'r','utf-8') as fp :
                line_num = 1;
                try:
                    for line in fp.readlines():
                        if ptn.search(line): print(fname,line_num,line),
                        line_num += 1;
                        #print(fname,line_num);
                except UnicodeDecodeError:
                    print("エンコードエラーで検索できませんでした．")
                finally:
                    #想定外は何もしない．(本来は例外をスローするなどの工夫が必要)
                    pass
            fp.close();
            print('=検索終了=')
    
                    