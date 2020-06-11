import json
import logging
import logging.handlers

import app
import hashlib


def init_log():
    '''
    设置日志格式
    :return:
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_log = logging.StreamHandler()
    log_path = app.BASE_DIR + "/log/log.log"
    file_log = logging.handlers.TimedRotatingFileHandler(filename=log_path, when="midnight", interval=1, backupCount=1)
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s')
    console_log.setFormatter(fmt)
    file_log.setFormatter(fmt)
    logger.addHandler(console_log)
    logger.addHandler(file_log)


def md5Encode(str):
    '''
    md5加密
    :param str:
    :return:
    '''
    # 创建md5对象
    m = hashlib.md5()
    m.update(str)  # 传入需要加密的字符串进行MD5加密
    return m.hexdigest()



def load_register_json_data(filePath):
    '''
    获取注册数据
    :return:
    '''
    result = list()
    with open(file=filePath, mode="r", encoding="utf-8") as f:
        data = json.load(f)
        for temp in data:
            result.append(list(temp.values()))
    return result



