from flask import Flask


app = Flask(__name__)

@app.route('/')
def login():
    return '测试登陆'



if __name__ == '__main':
    app.debug()
    app.run()