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
        '', 'Index', # 首页
        '/upload/', 'Upload', # 上传页面
        '/(\d+)/', 'View', # 图片页面
        '/delete/(\d+)/', 'Delete', # 删除图片
        '/random/', 'Random', # 随机图片
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
        import StringIO

        import Image

        # 略缩图大小
        size = (75, 75)
        #文件目录
        # fd = os.path.realpath(filedir)
        #文件扩展名
        ext = os.path.splitext(filename)[1]
        #定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '%d' % random.randint(0, 100)
        #重写合成文件名
        # filename = os.path.join(fd, fn + ext)
        filename = filedir + '/' + fn + ext
        thumb_name = filedir + '/thumb/' + fn + ext
        with open(filename, 'wb') as fout:
            fout.write(content)
        im = Image.open(StringIO.StringIO(content))
        im.thumbnail(size)
        im.save(thumb_name, im.format)
        return (filename, thumb_name)

    def POST(self):
        """处理发送过来的表单数据
        """
        post_data = web.input(upfile={})
        # 图片保存目录
        filedir = 'static'
        # print post_data
        # print post_data.imgfile.filename
        # 文件路径
        filepath = post_data['upfile'].filename.replace('\\', '/')
        # 文件名称
        filename = filepath.split('/')[-1]
        # 文件内容
        image_content = post_data['upfile'].file.read()
        # save_path = self.save_file(filedir, filename, image_content)
        # 保存后的图片路径
        image_path, thumb_path = self.save_file(filedir, filename,
                image_content)
        # image_path = '/' + save_path[0]
        # thumb_path = '/' + save_path[1]
        # des = post_data['description']
        orig_des = post_data['orig-description']
        orig_link = post_data['orig-link']
        up_user = post_data['up-user']
        # 获取最后一个图片的id
        image_id = ImageDB().get_image_id().maxid
        # 添加图片信息到数据库
        ImageDB().add_image(image_path, orig_des, orig_link,thumb_path, up_user)
        # 刚才添加的图片的id
        if image_id is None:
            image_id = ImageDB().get_image_id().maxid
        else:
            image_id += 1
        # print image_id
        return render.upload('/'+ str(image_id) +'/')


class View(object):
    """查看图片
    """
    def GET(self, image_id):
        """GET method
        """
        image_id = int(image_id)
        print image_id
        # 获取图片信息
        image_info = ImageDB().get_image_info(image_id)
        # 获取上一个及下一个图片的id
        image_next = ImageDB().get_image_next(image_id)
        image_more = ImageDB().get_all(limit=3)
        # print image_info
        # print image_next
        # 如果id不存在
        if image_info is None:
            return web.notfound()
        else:
            ImageDB().update_visit(image_id)
        return render.photo(image_info, image_next, image_more)


class Random(object):
    """随机图片id
    """
    def GET(self):
        random_id = ImageDB().get_all(limit=1)[0].image_id
        print random_id
        web.seeother('/' + str(random_id) + '/')


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()

