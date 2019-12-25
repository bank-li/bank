'''
引用日期时间 和libs里的SQLAlchemy
ORM:对象关系映射
最有名的ORM框架是SQLAlchemy

追踪-->libs.db
'''
from datetime import datetime

from libs.db import db

#定义Weibo对象
class Weibo(db.Model):
    #表的名字
    __tablename__ = 'weibo'

    #表的结构
    id = db.Column(db.Integer,primary_key=True)  #主键
    uid = db.Column(db.Integer,nullable=False) #不可空类型
    content = db.Column(db.Text)  #内容为文本类型
    created = db.Column(db.DateTime,default=datetime.now)  #发布时间
    updated = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)  #更新时间为当前时间