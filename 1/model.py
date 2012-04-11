#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

"""与图片有关的数据库操作
"""
import web
import conf

db_args = conf.db_args
db = web.database(**db_args)
app = conf.app
site = conf.site


class Logged(object):
    """根据 cookies 判断登录信息
    """
    def set_cookies(self):
        web.setcookie('login', 1, 2*60*60)
    def del_cookies(sefl):
        web.setcookie('login', 0, -1)
    def logged(self):
        """根据 cookies 判断是否登录
        """
        try:
            if web.cookies().login == '1':
                print 'True'
                return True
            else:
                return False
        except:
            return False


config = web.storage({
    'site': site,
#    static: '/static',
    'logged': Logged(),
})
web.template.Template.globals['config'] = config
web.template.Template.globals['str'] = str


class ImageDB(object):
    """图片数据库操作
    """
    def get_random(self, limit=3):
        """随机图片
        """
        from random import sample
        # 以下适用于少量数据
        # all_id = db.select('image')
        # if len(all_id) <= limit:
            # return all_id
        # else:
            # return sample(all_id, limit) # 随机获取 limit 个元素
        # 大量数据
        count_id = db.select('image',
                        what='count(image_id) as count')[0].count
        if count_id <= limit:
            return db.select('image')
        else:
            return tuple((db.select('image', order='image_id',
                        offset='$id_', limit=1, vars=locals())[0]
                        for id_ in sample(xrange(count_id), limit)))

    def get_all_new(self, limit=10):
        """最新图片
        """
        return tuple(db.select('image', limit=limit,
                                order='image_id desc'))

    def get_all_hot(self, limit=5):
        """最热图片
        """
        return tuple(db.select('image', limit=limit,
                                order='visit desc'))

    def get_all_like(self, limit=5):
        """最受欢迎图片
        """
        return tuple(db.select('image', limit=limit,
                                order='likes desc'))

    def get_image_info(self, image_id):
        """图片信息
        """
        try:
            return tuple(db.select('image', where='image_id=$image_id',
                                vars=locals()))[0]
        except IndexError:
            return None

    def get_image_next(self, image_id):
        """相邻图片
        """
        try:
            before = tuple(db.select('image', what='image_id',
                    where='image_id<$image_id',limit=1,
                    order='image_id desc', vars=locals()))[0]
        except IndexError:
            before = web.storage({})
        try:
            after = tuple(db.select('image', what='image_id',
                    where='image_id>$image_id',
                    limit=1, order='image_id', vars=locals()))[0]
        except IndexError:
            after = web.storage({})
        return web.storage({'before': before, 'after': after})
    
    def add_image(self, img, description, link, thumb, user):
        """添加图片, 返回id值
        """
        return db.insert('image', img=img, description=description,
                link=link, thumb=thumb, username=user)

    def update_visit(self, image_id):
        """访问数
        """
        db.query('update image set visit=visit+1 where image_id=$image_id',
                        vars=locals())
    
    def update_like(self, image_id):
        """喜爱数
        """
        db.query('update image set likes=likes+1 where image_id=$image_id',
                        vars=locals())

    def delete_image(self, image_id):
        """删除图片
        """
        db.delete('image', where="image_id=$image_id", vars=locals())

class ImageMime(object):
    """判断图片Mime类型
    """
    def __init__(self):
        self.GIF = "image/gif"
        self.JPEG = "image/jpeg"
        self.TIFF = "image/tiff"
        self.PNG = "image/png"
        self.BMP = "image/bmp"
        self.ICO = "image/x-icon"
        self.UNKNOWN = "application/octet-stream"

    def get_image_type(self, binary):
        size = len(binary)
        if size >= 6 and binary.startswith("GIF"):
            return self.GIF
        elif size >= 8 and binary.startswith("\x89PNG\x0D\x0A\x1A\x0A"):
            return self.PNG
        elif size >= 2 and binary.startswith("\xff\xD8"):
            return self.JPEG
        elif (size >= 6 and (binary.startswith("II*\x00") or
                             binary.startswith("MM\x00*")
                             )):
            return self.TIFF
        elif size >= 2 and binary.startswith("BM"):
            return self.BMP
        elif size >= 4 and binary.startswith("\x00\x00\x01\x00"):
            return self.ICO
        else:
            return self.UNKNOWN


class UserDB(object):
    """操作用户信息数据库
    """
    def verify_user(self, username, password):
        """用户验证
        """
        # where_dict = {'user_name': username, 'user_pass': password}
        # return db.select('users', what="user_id",
                    # where=web.db.sqlwhere(where_dict), vars=locals())[0]
        return tuple(db.select('users', what='name',
                where='name=$username and pass=$password',
                vars=locals()))[0]

    def add_user(self, user_info):
        """添加用户
        """
        pass
    
    def del_user(self, user_id):
        """删除用户
        """
        pass
    
    def update_user(self, user_info):
        """更新用户
        """
        pass


class Encrypt(object):
    """
    """
    def __init__(self):
        pass
    
    def encrypt_pass(self):
        """
        """
        pass
    
    def encrypt_cookie(self):
        """
        """
        pass
    
