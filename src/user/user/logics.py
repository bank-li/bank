#完成注册页面

'''
1.找到图片路径
2.下载
3.保存
'''

import os  #系统，用于路径
from functools import wraps  #计算

from flask import session
from flask import redirect   #重定向 ，跳转
from flask import render_template  #模板渲染,指的是HTML页面

def save_avater(nickname,avater_file):
    '''保存头像'''
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir,'static','upload',nickname)
    avater_file.save(file_path)

def login_required(view_func):
    '''登陆验证装饰器'''
    @wraps(view_func)
    def check(*args,**kwargs):
        if 'uid' in session:         #检查uid是否在session里，有的话返回内容，没有就跳转到登陆页面

            return view_func(*args,**kwargs)
        else:
            return render_template('login.html',error='请您先登陆')

    return check
