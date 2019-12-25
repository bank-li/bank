#创建Use模块

from libs.db import db

class User(db.Model):
    '''用户表'''
    __tablename__ = 'user'  #定义表名

    id = db.Column(db.Integer,primary_key=True) #主关键字
    nickname = db.Column(db.String(20),unique=True,nullable=False,index=True) #唯一的，不能为空，索引
    password = db.Column(db.String(128),Tnullable=False) #不能为空
    gender = db.Column(db.String(10),default='unknow') #默认值
    bio = db.Column(db.String(200))
    city = db.Column(db.String(16),default='上海') #默认是上海
    avater = db.Column(db.String(128))
    birthday = db.Column(db.Date,default='1990-01-01')
    #创建日期
    created = db.Column(db.DateTime)


