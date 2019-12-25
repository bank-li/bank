from flask import Flask
from flask import redirect
from flask import render_template
from libs.db import db

app = Flask(__name__)
app.secret_key = 'M\xd2\x16\xa0K\x01\x0f@\x9f(\xab2V\xd7\xe3\x00'

#初始化数据库
#config 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

#创建蓝图
@app.route('/')
def home():
    return redirect('/weibo/')

if __name__ == '__main__':

    #蓝图分支
    from user import user_bp
    app.register_blueprint(user_bp,url_prefix='/user')

    from weibo import weibo_bp
    app.register_blueprint(weibo_bp,url_prefix='/weibo')
    app.debug = True
    app.run()