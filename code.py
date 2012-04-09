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
from model import UserDB

# 链接设置
urls = (
        '/', 'Index', # 首页
        '/upload/', 'Upload', # 上传页面
        '/(\d+)/', 'View', # 图片页面
        '/delete/(\d+)/', 'Delete', # 删除图片
        '/random/', 'Random', # 随机图片
        '/login/', 'Login', # 登录
        '/logout/', 'Logout', # 退出
        )


# web.config.debug = False

app = web.application(urls, globals())

# 调试模式下使用 session
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0})
    web.config._session = session
else:
    session = web.config._session

# AttributeError: 'ThreadedDict' object has no attribute 'login'
# print session.login


class Logged(object):
    """
    """
    def logged(self):
        """根据 session 判断是否登录
        """
        if session.login == 1:
            return True
        else:
            return False

t_globals = {
    'session': session,
    'logged_': Logged(),
}
# 模板
render = web.template.render('templates', base='base', globals=t_globals)


class Index(object):
    """首页
    """
    def GET(self):
        """GET
        """
        news = ImageDB().get_all_new(limit=10)
        hots = ImageDB().get_all_hot(limit=5)
        likes = ImageDB().get_all_like(limit=5)
        return render.index(news, hots, likes)


class Upload(object):
    """上传页面
    """
    def GET(self):
        """GET
        """
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
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        if not os.path.isdir(os.path.dirname(thumb_name)):
            os.makedirs(os.path.path.dirname(thumb_name))
        with open(filename, 'wb') as fout:
            fout.write(content)
        im = Image.open(StringIO.StringIO(content))
        x, y = im.size
        rex = 75
        rey = 75
        print x, y
        x, y = (rex, (float(rex)/x)*y) # 等比例缩放后的尺寸
        print x, y
        if rey > y:
            rey = int(y)
        im.thumbnail((x, y))
        box = (0, 0, rex, rey)
        im = im.crop(box) # 剪切
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
        # 添加图片信息到数据库
        ImageDB().add_image(image_path, orig_des, orig_link,thumb_path, up_user)
        # 刚才添加的图片的id
        image_id = ImageDB().get_image_id().maxid
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
        image_more = ImageDB().get_random(limit=3)
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
        """GET
        """
        random_id = ImageDB().get_random(limit=1)[0].image_id
        print random_id
        raise web.seeother('/' + str(random_id) + '/')


class Delete(object):
    """删除图片
    """
    def GET(self, image_id):
        """GET
        """
        if not Logged().logged():
            return web.unauthorized()
        ImageDB().delete_image(image_id)
        # raise web.seeother('/' + str(image_id) + '/')
        raise web.seeother('/')


class Login(object):
    """用户登录
    """
    def GET(self):
        """GET
        """
        # 来源链接
        # TODO 判断来源链接是否为当前站点，不是则跳到首页
        referer = web.ctx.env.get('HTTP_REFERER', '/')
        print referer
        if Logged().logged():
            if '/login/' in referer:
                raise web.seeother('/')
            else:
                raise web.seeother(referer)
        else:
            return render.login(referer)

    
    def POST(self):
        """POST method
        """
        user, passwd = web.input().user, web.input().passwd
        # 来源链接
        referer = web.input().referer
        if user and passwd:
            try:
                ident = UserDB().verify_user(user, passwd)
                session.login = 1
                raise web.seeother(referer)
                # return 'ok'
            except:
                # session.login = 0
                raise web.seeother('/login/')
        else:
            raise web.seeother('/login/')



class Logout(object):
    """退出登录
    """
    def GET(self):
        session.login=0
        session.kill()
        raise web.seeother('/')


if __name__ == '__main__':
    app.run()

