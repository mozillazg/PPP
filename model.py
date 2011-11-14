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
                                order='like desc')
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

    def add_image(self, image_path, image_description,
            orig_description, orig_link, up_user=''):
        """添加图片
        """
        self.db.insert('image', image_path = image_path,
                image_description = image_description,
                orig_description = orig_description,
                orig_link = orig_link, up_user = up_user)

    def update_visit(self, image_id):
        """访问数
        """
        self.db.query('update image set visit=visit+1 where image_id=$image_id')
    def update_like(self, image_id):
        """喜爱数
        """
        self.db.query('update image set like=like+1 where image_id=$image_id')
