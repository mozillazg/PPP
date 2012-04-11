#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
"""main file
"""

import web
import sae
import conf
import model


render = conf.render
debug = conf.local_debug


class Redirect(object):
    """
    """
    def GET(self, path):
        web.seeother('/' + path)


class Index(object):
    """首页
    """
    def GET(self):
        """GET
        """
        news = model.ImageDB().get_all_new(limit=10)
        hots = model.ImageDB().get_all_hot(limit=5)
        likes = model.ImageDB().get_all_like(limit=5)
        return render.index(news, hots, likes)


class Upload(object):
    """上传页面
    """
    def GET(self):
        """GET
        """
        return render.upload()
        
    def gen_thumb(self, img, resize=None):
        """生成略缩图
        img: 图片数据
        resize: 略缩图大小(x, y)，默认(75, 75)
        """
        import StringIO
        import tempfile
        if debug:
            import Image
        else:
            from PIL import Image

        im = Image.open(StringIO.StringIO(img))
        x, y = im.size
        # 略缩图大小
        if resize is None:
            rex, rey = 75, 75
        else:
            rex, rey = resize
        if rex > x:
            rex = int(x)
        if rey > y:
            rey = int(y)
        x, y = (rex, (float(rex)/x)*y) # 等比例缩放后的尺寸
        print x, y
        if rey > y:
            rey = int(y)
        # 缩放图片
        im.thumbnail((x, y), Image.ANTIALIAS) # 高清略缩图
        box = (0, 0, rex, rey) # 从左上角开始切图
        im = im.crop(box) # 剪切
        thumb_name = StringIO.StringIO()
#        im.save(thumb_name, 'jpeg', quality = 95)
        im.save(thumb_name, 'png')
#        thumb = open(thumb_name, 'rb').read()
        thumb = thumb_name.getvalue()
        thumb_name.close()
        return thumb

    def POST(self):
        """处理发送过来的表单数据
        """
        post_data = web.input(upfile={})
        # 文件内容
        image = post_data['upfile'].file.read()
        orig_des = post_data['orig-description']
        orig_link = post_data['orig-link']
        up_user = post_data['up-user']
        thumb = self.gen_thumb(image)
        try:
            # 添加图片信息到数据库
            image_id = model.ImageDB().add_image(
                    image, orig_des, orig_link,thumb, up_user)
        except:
            return '图片上传失败！'
        else:
            return render.upload('/'+ str(image_id))


class ShowImage(object):
    """show image
    """
    def __init__(self):
        self.imagedb = model.ImageDB()
        self.get_image_mime = model.ImageMime().get_image_type

    def GET(self, img_id):
        img_id = int(img_id)
        image_info = self.imagedb.get_image_info(img_id)
        if image_info:
            # 显示图片
            image_mime = self.get_image_mime(image_info.img)
            web.header('Content-Type', image_mime)
            return image_info.img
        else:
            return web.notfound()


class ShowThumb(object):
    """show thumb
    """
    def __init__(self):
        self.imagedb = model.ImageDB()
        self.get_image_mime = model.ImageMime().get_image_type

    def GET(self, img_id):
        img_id = int(img_id)
        image_info = self.imagedb.get_image_info(img_id)
        if image_info:
            image_mime = self.get_image_mime(image_info.thumb)
            web.header('Content-Type', image_mime)
            return image_info.thumb
        else:
            return web.notfound()

class View(object):
    """查看图片
    """
    def GET(self, image_id):
        """GET method
        """
        image_id = int(image_id)
        print image_id
        # 获取图片信息
        image_info = model.ImageDB().get_image_info(image_id)
        # 获取上一个及下一个图片的id
        image_next = model.ImageDB().get_image_next(image_id)
        image_more = model.ImageDB().get_random(limit=3)
        # print image_info
        # print image_next
        # 如果id不存在
        if image_info is None:
            return web.notfound()
        else:
            model.ImageDB().update_visit(image_id)
        return render.photo(image_info, image_next, image_more)


class Random(object):
    """随机图片id
    """
    def GET(self):
        """GET
        """
        random_id = model.ImageDB().get_random(limit=1)[0].image_id
        print random_id
        raise web.seeother('/' + str(random_id))


class Delete(object):
    """删除图片
    """
    def GET(self, image_id):
        """GET
        """
        if not model.Logged().logged():
            return web.unauthorized()
        model.ImageDB().delete_image(image_id)
        # raise web.seeother('/' + str(image_id))
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
        # print referer
        if model.Logged().logged():
            if '/login' in referer:
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
                user = model.UserDB().verify_user(user, passwd)
                model.Logged().set_cookies()
                print 'ok'
                print referer
                web.seeother(referer)
            except:
                print 'error'
                raise web.seeother('/login')
        else:
            raise web.seeother('/login')



class Logout(object):
    """退出登录
    """
    def GET(self):
        model.Logged().del_cookies()
        raise web.seeother('/')

