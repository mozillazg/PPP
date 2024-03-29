#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

"""与图片有关的数据库操作
"""

import web

class ImageDB(object):
    """图片数据库操作
    """
    def __init__(self):
        self.db = web.database(dbn='postgres', db='ppp',
                                user='postgres', pw='py')
    
    def get_random(self, limit=3):
        """随机图片
        """
        from random import sample
        # 以下适用于少量数据
        # all_id = self.db.select('image')
        # if len(all_id) <= limit:
            # return all_id
        # else:
            # return sample(all_id, limit) # 随机获取 limit 个元素
        # 大量数据
        count_id = self.db.select('image', what='count(image_id) as count')[0].count
        if count_id <= limit:
            return self.db.select('image')
        else:
            # randoms = []
            # 利用 offset 和 limit 取得第 n 条数据
            # for id_ in sample(xrange(count_id), limit):
                # random_ = self.db.select('image', order='image_id desc',
                                # offset='$id_', limit=1, vars=locals())[0]
                # randoms.append(random_)
            # return randoms
            return [self.db.select('image', order='image_id',
                        offset='$id_', limit=1, vars=locals())[0]
                        for id_ in sample(xrange(count_id), limit)]

    def get_all_new(self, limit=10):
        """最新图片
        """
        return self.db.select('image', limit=limit,
                                order='image_id desc')
    
    def get_all_hot(self, limit=5):
        """最热图片
        """
        return self.db.select('image', limit=limit,
                                order='visit desc')
    
    def get_all_like(self, limit=5):
        """最受欢迎图片
        """
        return self.db.select('image', limit=limit,
                                order='likes desc')
    
    def get_image_info(self, image_id):
        """图片信息
        """
        try:
            return self.db.select('image', where='image_id=$image_id',
                                vars=locals())[0]
        except IndexError:
            return None
    
    def get_image_next(self, image_id):
        """相邻图片
        """
        try:
            before = self.db.select('image', what='image_id',
                    where='image_id<$image_id',limit=1,
                    order='image_id desc', vars=locals())[0]
        except IndexError:
            before = web.storage({})
        try:
            after = self.db.select('image', what='image_id',
                    where='image_id>$image_id',
                    limit=1, order='image_id', vars=locals())[0]
        except IndexError:
            after = web.storage({})
        return web.storage({'before': before, 'after': after})
    
    def get_image_id(self):
        """获取最后上传的图片的id
        """
        return self.db.query('select max(image_id) as maxid from image')[0]
    
    def add_image(self, img, description, link, thumb, user=''):
        """添加图片
        """
        self.db.insert('image', img=img, description=description,
                link=link, thumb=thumb, username=user)
    
    def update_visit(self, image_id):
        """访问数
        """
        self.db.query('update image set visit=visit+1 where image_id=$image_id',
                        vars=locals())
    
    def update_like(self, image_id):
        """喜爱数
        """
        self.db.query('update image set likes=likes+1 where image_id=$image_id',
                        vars=locals())

    def delete_image(self, image_id):
        """删除图片
        """
        import os
        image_info = self.db.select('image', where='image_id=$image_id',
                                vars=locals())[0]
        if image_info is not None:
            img_path = image_info.img
            thumb_path = image_info.thumb
            if os.path.isfile(img_path):
                os.remove(img_path)
            if os.path.isfile(thumb_path):
                os.remove(thumb_path)
            self.db.delete('image', where="image_id=$image_id",
                    vars=locals())


class UserDB(object):
    """操作用户信息数据库
    """
    def __init__(self):
        self.db = web.database(dbn='postgres', db='ppp',
                                user='postgres', pw='py')
    
    def verify_user(self, username, password):
        """用户验证
        """
        # where_dict = {'user_name': username, 'user_pass': password}
        # return self.db.select('user_', what="user_id",
                    # where=web.db.sqlwhere(where_dict), vars=locals())[0]
        return self.db.select('user_', what='user_id',
                where = 'user_name=$username and user_pass=$password',
                vars = locals())[0]

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
    
