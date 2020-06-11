import logging
import unittest

import requests
import pymysql
from parameterized import parameterized

import app
from api.register_api import RegisterApi
from utils import md5Encode, load_register_json_data


def findUserByMobile(mobile):
    '''
    根据参数查询数据库中注册时用户的手机号和密码并返回
    :param mobile:
    :return:
    '''
    try:

        conn = pymysql.connect(host="localhost", user="root", database="tpshop2.0", port=3306, charset="utf8")
        curson = conn.cursor()
        sql = "select mobile,`password`from tp_users WHERE mobile=" + "'" + mobile + "'"
        curson.execute(sql)
        result = curson.fetchone()
        return result
    except Exception as ex:
        logging.info("*******************查询数据失败，原因为：{}".format(ex))
        return None
    finally:
        curson.close()
        conn.close()


class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registerApi = RegisterApi()
        cls.register_url = "http://localhost/index.php/Home/User/reg.html"
        cls.login_url = "http://localhost/index.php?m=Home&c=User&a=do_login"
        cls.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def setUp(self):
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def assert_result(self, http_code, status, expect_result, response):
        '''
        断言封装
        :param http_code:
        :param status:
        :param expect_result:
        :param response:
        :return:
        '''
        self.assertEqual(http_code, response.status_code)
        self.assertEqual(status, response.json().get("status"))
        self.assertIn(expect_result, response.json().get("msg"))

    @parameterized.expand(load_register_json_data(app.BASE_DIR + "/data/register_data.json"))
    def test_register(self, request_body, http_code, status, register_msg, login_msg):
        '''
        注册并登陆
        :param request_body:
        :param http_code:
        :param status:
        :param register_msg:
        :param login_msg:
        :return:
        '''
        # 获取注册验证码
        response = self.registerApi.doGet(self.session, app.REGISTER_VERIFY_URL)
        logging.info("*******************获取注册验证码成功的Content-Type的值为：{}".format(response.headers.get("Content-Type")))
        response = self.registerApi.doFormPost(self.session, self.register_url, request_body, headers=self.headers)
        logging.info("*******************注册成功的结果为：{}".format(response.json()))
        # 注册相关断言
        self.assert_result(http_code, status, register_msg, response)

        # 与数据库的用户名和密码数据进行断言
        db_username, db_password = findUserByMobile(request_body.get("username"))  # 获取数据库里的用户名及密码
        self.assertIn(request_body.get("username"), db_username)
        pwd = "TPSHOP" + request_body.get("password")
        self.assertIn(md5Encode(pwd.encode("utf-8")), db_password)  # md5加密之后再与数据库里的密码进行校验

        # 获取登陆的验证码
        response = self.registerApi.doGet(self.session, app.LOGIN_VERIFY_URL)
        logging.info("*******************获取登陆证码成功的Content-Type的值为：{}".format(response.headers.get("Content-Type")))
        login_data = {"username": request_body.get("username"),
                      "password": request_body.get("password"),
                      "verify_code": request_body.get("verify_code")
                      }  # 取参数化的数据

        response = self.registerApi.doFormPost(self.session, self.login_url, login_data, headers=self.headers)
        logging.info("*******************登陆成功的结果为：{}".format(response.json()))

        # 登陆相关断言
        self.assert_result(http_code, status, login_msg, response)
