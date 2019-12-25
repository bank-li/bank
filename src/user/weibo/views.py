'''
蓝图是Flask应用程序组件化的方法，可以在一个应用内或跨越多个项目
共用蓝图，简化开发难度

1.我们在一个文件中写入多个路由，代码繁多，维护不便
2.蓝图：
        把一个项目分成一个个单独的app，每个app具有自己相应的功能，通过
        路由将他们连接成一个大项目
3.做法：
        1.创建主路由配置文件 manage.py
        from flask import Flask
        app = Falsk(__name__)   #创建Flask的主app

        #创建路由
        @app.route('/')
        def index():
            return 'hello world'

        @app.route('/list')
        def list():
            return 'list'

        if __name__ == '__main__'
            app.run(host='192.168.1.208')  #启动项目

        2.在manage.py平级目录下创建两个文件admin.py  user.py

        from flask import Blueprint  #导入蓝图

        user = Blueprint('user',__name__)  #创建一个蓝图，必须是两个参数，分别是蓝图名称和蓝图所在模块

        #用蓝图来设置路由
        @user.route('/user/bank')
        def bank():
            return 'handsome'

        3.回到主程序manage.py进行添加关联两个蓝图的内容

        from flask import Flask

        from admin import admin  ####将刚刚创建的admin，user两个蓝图添加过来
        from user import user

        app = Falsk(__name__)   #创建Flask的主app

        app.register_blueprint(admin)
        app.register_blueprint(user)   ###把创建的蓝图继续添加到主程序app中，这样运行起来才能继承


        #创建路由
        @app.route('/')
        def index():
            return 'hello world'

        @app.route('/list')
        def list():
            return 'list'

        if __name__ == '__main__'
            app.run(host='192.168.1.208')  #启动项目

'''
import datetime
from math import ceil   #得到的结果向上取整

from flask import abort   #终止计划
from flask import request   #请求
from flask import session   #服务器中存储用户登陆信息的地方

from flask import redirect   #重定向，跳转的功能
from flask import Blueprint   #蓝图
from flask import render_template   #渲染模板

from .models import Weibo
from user.models import User
from libs.db import db
from user.logics import login_required

weibo_bp = Blueprint('weibo',import_name='weibo')
weibo_bp.template_folder = './templates'

@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    '''显示最新的前50条微博'''
    #获取微博数据
    page = int(request.args.get('page',1))              #page标页码，这里指定第一页
    n_per_page = 10
    offset = (page - 1) * n_per_page
    #当前页要显示的微博
    #select * from weibo order by updated desc limit 10 offset 20;
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(10).offset(offset)  #微博查询排序     更新倒序      最大为10
    n_weibo = Weibo.query.count()     #微博总数
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)   #总页数  ceil:前面引用的数学公式向上取整

    #获取微博对应的作者
    uid_list = {wb.uid for wb in wb_list}   #取出微博对应的用户id
    #select id,nickname from user id in ...
    user = dict(User.query.filter(User.id.in_(uid_list)).values('id','nickname'))   #字典用户id和名字
    return render_template('index.html',page=page,n_page=n_page,wb_list=wb_list,user=user)

@weibo_bp.route('/post',method=('POST','GET'))
@login_required   #引用装饰器，判断是否登陆
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()                    #判断是不是post请求，去过是就获取内容，如果没有内
        if not content:                                                  # 容，就返回post.html页面，提示不能为空，如果不是
            return render_template('post.html',error='微博内容不能为空')   #post请求，就直接返回post.html页面
        else:
            weibo = Weibo(uid=session['uid'],content=content)
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/shoow?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/edit')
@login_required       #装饰器，判断是否登陆
def edit():
    if request.method == 'POST':                            #如果是post请求方式，就获取发送微博的id和内容，
        wid = int(request.form.get('wid'))                  #如果没有内容，返回到post.html,并提示微博不能为空
        content = request.form.get('content').strip()       #有过有内容就把一系列内容提交上去
        if not content:
            return render_template('post.html',error='微博内容不允许为空')
        else:
            weibo = Weibo.query.get(wid)
            weibo.content = content
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)    #跳转到此地址
    else:
        wid = int(request.args.get('wid'))                  #如果不是post请求，通过wid找到weibo就返回到edit.html和 weibo
        weibo = Weibo.query.get(wid)
        return render_template('edit.html',weibo=weibo)


@weibo_bp.route('/show')                       #蓝图，找到微博，如果微博为空，扔一个404，如果不为空就显示到show.html
def show():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    if weibo is None:
        abort(404)
    else:
        user = User.query.get(weibo.uid)
        return render_template('show.html',weibo=weibo,user=user)


@weibo_bp.route('/delete')
@login_required     #装饰器
def delete():       #删除微博的id并提交，返回到首页
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('/')



