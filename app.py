# 设置获取验证码的全局变量
import os

import pymysql

REGISTER_VERIFY_URL = "http://localhost/index.php?m=Home&c=User&a=verify&type=user_reg"
LOGIN_VERIFY_URL = "http://localhost/index.php?m=Home&c=User&a=verify"

# 设置变量存储当前项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



