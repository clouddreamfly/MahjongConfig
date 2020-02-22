#!/usr/bin/python
#-*-coding:utf-8-*-

from distutils.core import setup
import glob
import py2exe


options = {"py2exe": {	
		"compressed": 1, #压缩  
		"optimize": 2, 
		"bundle_files": 1 #所有文件打包成一个exe文件
	}
}   

setup(
    windows = [{"script": "MahjongConfig.py", "icon_resources": [(1, "images/mahjong.ico")]}],
	options = options,
	data_files = [
		('images',['images/mahjong.ico']),
		('images/mj_bg', glob.glob('images/mj_bg/*.*')),
		('images/mj_left',glob.glob('images/mj_left/*.*')),
		('images/mj_right',glob.glob('images/mj_right/*.*')),
		('images/mj_top',glob.glob('images/mj_top/*.*')),
		('images/mj_bottom',glob.glob('images/mj_bottom/*.*'))],
    zipfile = None,
) 


