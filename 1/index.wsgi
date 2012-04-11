#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 在index.wsgi最前面打上这个patch，可以临时绕过本地文件系统的tempfile
# 但是需要注意上传文件过大的问题
# Monkey patch for tempfile.TemporaryFile
# http://tocode.sinaapp.com/32
import os
 
import tempfile
import cStringIO
 
def TemporaryFile(mode='w+b', bufsize=-1, suffix="",
prefix='', dir=None):
    return cStringIO.StringIO()
tempfile.TemporaryFile = TemporaryFile
 
#import sae
#import sae.storage


import sae
import web
import conf

#urls = conf.URLS
app = conf.app
#app = web.application(urls, globals())
application = sae.create_wsgi_app(app.wsgifunc())

