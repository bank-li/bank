#完成注册页面

'''
1.找到图片路径
2.下载
3.保存
'''

import os

def save_avater(nickname,avater_file):
    '''保存头像'''
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir,'static','upload',nickname)
    avater_file.save(file_path)
