#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import os
import tempfile
import web
import sae

# 调试模式
web.config.debug = True
APP_NAME = os.environ.get('APP_NAME', '')
# 本地调试
local_debug = not APP_NAME

# 域名
if local_debug:
    site = 'http://localhost:8080'
else:
    site = 'http://%s.sinaapp.com' %(APP_NAME)

# 配置URL
urls = (
    '/(.*)/', 'view.Redirect',
    '/', 'view.Index', # 首页
    '/upload', 'view.Upload', # 上传页面
    '/image/(\d+)', 'view.ShowImage', # show image
    '/thumb/(\d+)', 'view.ShowThumb',
    '/(\d+)', 'view.View', # 图片页面
    '/delete/(\d+)', 'view.Delete', # 删除图片
    '/random', 'view.Random', # 随机图片
    '/login', 'view.Login', # 登录
    '/logout', 'view.Logout', # 退出
)

# 配置数据库
if local_debug:
    db_args = dict(
        dbn = 'mysql',
        db = 'ppperson',
        user = 'root',
        pw = 'root',
        host = 'localhost',
        port = 3306
    )
else:
    db_args = dict(
        dbn = 'mysql',
        db = sae.const.MYSQL_DB,
        user = sae.const.MYSQL_USER,
        pw = sae.const.MYSQL_PASS,
        host = sae.const.MYSQL_HOST,
        port = int(sae.const.MYSQL_PORT) # 端口一定要是 int(str)
        # connect_timeout = 5
        # unicode
    )

app = web.application(urls, globals())
render = web.template.render('templates/', base='base',)

