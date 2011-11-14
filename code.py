#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
"""main file
"""

import web
from model import ImageDB

# 链接设置
urls = (
        '', 'Index',
        '/upload/', 'Upload',
        '/(\d+)/', 'View',
        '/delete/(\d+)/', 'Delete',
        )

# 模板
render = web.template.render('templates', base='base')

class Upload(object):
    """上传页面
    """
    def GET(self):
        return render.upload()
    def save_file(self, filedir, filename, content):
        """保存文件
        """
        import os
        import time
        import random
        #文件目录
        # fd = os.path.realpath(filedir)
        #文件扩展名
        ext = os.path.splitext(filename)[1]
        #定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        #重写合成文件名
        # filename = os.path.join(fd, fn + ext)
        filename = filedir + '/' + fn + ext
        fout = open(filename, 'wb')
        fout.write(content)
        fout.close()
        return filename

    def POST(self):
        post_data = web.input(upfile={})
        filedir = 'static'
        # print post_data
        # print post_data.imgfile.filename
        filepath = post_data['upfile'].filename.replace('\\', '/')
        filename = filepath.split('/')[-1]
        image_content = post_data['upfile'].file.read()
        image_path = '/' + self.save_file(filedir, filename, image_content)
        des = post_data['description']
        orig_des = post_data['orig-description']
        orig_link = post_data['orig-link']
        up_user = post_data['up-user']
        image_id = ImageDB().get_image_id().maxid
        if image_id is None:
            image_id = 0
        # print image_id
        ImageDB().add_image(image_path, des, orig_des, orig_link, up_user)
        image_id += 1
        return render.upload('/'+ str(image_id) +'/')

class View(object):
    """查看图片
    """
    def GET(self, image_id=0):
        image_id = int(image_id)
        print image_id
        image_info = ImageDB().get_image_info(image_id)
        image_next = ImageDB().get_image_next(image_id)
        # print image_info
        # print image_next
        if image_info is None:
            return web.notfound()
        return render.photo(image_info, image_next)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()

