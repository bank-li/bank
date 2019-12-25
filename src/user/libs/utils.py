#完成了注册页面

'''
    引用随机数和哈希算法进行密码加密
1.把密码转化成utf8
2.然后计算成哈希值
3.再弄出来一个后8位随机数
4.把哈希值和随机数连接起来
'''

import random
from hashlib import sha256

def gen_password(user_password):
    '''产生了一个安全的密码'''
    bin_password = user_password.encode('utf8') #把密码转成bytes类型
    hash_value = sha256(bin_password).hexdigest() #计算用户密码的哈希值
    salt = '%x' % random.randint(0x100000000,0xffffffff) #产生随机盐
    safe_password = salt + hash_value
    return safe_password

def check_password(user_password,safe_password):
    '''检查用户密码是否正确'''
    bin_password = user_password.encode('utf8') #把密码转成bytes类型
    hash_value = sha256(bin_password).hexdigest() #计算用户密码的哈希值

    return hash_value == safe_password[8:]