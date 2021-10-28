# !/usr/bin/python3
# coding=utf-8

import pymysql
import config
import json
import threading
from functools import wraps


# 单例装饰器 可用__new__ 魔术方法实现
def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


# 个人信息存储
@singleton
class Storage:
    # 数据缓冲区，较少io压力
    __buf = []
    # 缓冲区大小， 配置文件中定义
    __BUF_MAX = config.BUF_MAX

    # 初始化数据库连接
    def __init__(self):
        self.conn = pymysql.connect(host=config.DB_HOST,
                                    port=config.DB_PORT,
                                    user=config.DB_USERNAME,
                                    password=config.DB_PASS,
                                    database=config.DB_NAME,
                                    charset='utf8'
                                    )
        self.cursor = self.conn.cursor()
        self.__buf_lock = threading.Lock()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def flush(self):
        if len(self.__buf) < 100:
            return

        sql = "INSERT INTO `stu_info`(`name`, `sid`, `sex`, `college`, " \
              + "`class`, `email`, `phone`, `minor`, `type`, `qq`) VALUES " \
              + ",".join(self.__buf)

        try:
            # 执行sql语句
            self.cursor.execute(sql)

            # 提交到数据库执行, b并且清空缓冲区
            self.conn.commit()
            print(str(len(self.__buf)) + "条数据存入数据库")
            self.__buf = []
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.conn.rollback()

    # 存储个人信息到缓冲区
    def save(self, data):
        # 防止None破坏sql None无法被join连接,无法拼接sql
        for key in data:
            if data[key] is None:
                data[key] = ""

        # 整理顺序
        info = [data['xm'], data['xh'], data['xb'], data['yxmc'], data['bj'], data['email'], data['dh'], data['fxzy'],
                data['usertype'], str(data['qq'])]
        info = "('" + ("', '".join(info)) + "')"
        with self.__buf_lock:
            self.__buf.append(info)

        # 缓冲区过大则直接存入数据库
        if len(self.__buf) >= self.__BUF_MAX:
            with self.__buf_lock:
                self.flush()

