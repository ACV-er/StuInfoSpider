# !/usr/bin/python3
# coding=utf-8

import requests
import json
import config
import multiprocessing
from Storage import Storage
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def get_token():
    url = config.TARGET_URL
    param = {
        "method": "authUser",
        "xh": config.SID,
        "pwd": config.PASSWORD
    }

    r = requests.get(url, params=param)
    return json.loads(r.text)["token"]


def _get_info(sid, token):
    url = config.TARGET_URL
    param = {
        "method": "getUserInfo",
        "xh": sid
    }
    header = {
        "token": token
    }

    r = requests.get(url, params=param, headers=header)
    return json.loads(r.text)


def get_info(sid, token):
    try:
        return _get_info(sid, token)
    except Exception as e:
        print(e)


def get_all_college(grade, token, storage):
    for cls in range(config.CLASS_BEGIN, config.CLASS_END):
        flag = 0
        for stu in range(config.PERSON_BEGIN, 80):
            if flag > 3:
                break
            sid = grade + str(cls).zfill(2) + str(stu).zfill(2)
            stu_info = get_info(sid, token)

            if stu_info == {}:
                stu_info = get_info(sid, token)
                if stu_info == {}:  # 二次查询，防止失误
                    flag = flag + 1
                else:
                    flag = 0
                    storage.save(stu_info)
                    print(sid.zfill(2))
            else:
                flag = 0
                storage.save(stu_info)
                print(sid.zfill(2))


def get_all_grade(grade, token, storage):
    pool = ThreadPoolExecutor(max_workers=config.MAX_THREADS)
    theads = []
    # 将
    for gollege in range(config.COLLEGE_BEGIN, config.COLLEGE_END):
        theads.append(pool.submit(get_all_college, str(grade) + str(gollege).zfill(2), token, storage))

    wait(theads, return_when=ALL_COMPLETED)


if __name__ == "__main__":
    token = get_token()
    storage = Storage()
    grades = config.GRADE

    processes = []
    for grade in grades:
        processes.append(multiprocessing.Process(target=get_all_grade, args=(grade, token, storage,)))

    for process in processes:
        process.start()

    # 等待所有进程结束
    for process in processes:
        process.join()

    # 把未满的缓冲区内容存入数据库
    storage.flush()

    print("Done.")
