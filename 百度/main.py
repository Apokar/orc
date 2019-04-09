# -*- coding: utf-8 -*-
# @Time    : 2019/4/9 17:07
# @Author  : Apokar
# @Email   : Apokar@163.com
# @File    : main.py
# @Comment :
import base64
import os
import traceback

import requests


def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=CLIENT_ID&client_secret=CLIENT_SECRET'

    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    content = requests.get(host, headers=headers).json()
    if (content):
        # print(content)
        at = content['access_token']
    return at


def img_2_string(path, at, classifierId):
    try:
        # path = 'D:\PycharmProjects\orc\hau1.png'

        if path:
            post_url = 'https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise?access_token=' + str(at)

        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            # s = urllib.parse.quote(base64_data)
        data = {'image': base64_data,
                'classifierId': classifierId}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        content = requests.post(post_url, headers=headers, data=data).json()
        print(content)

        first = content['data']['ret'][0]['word']
        second = content['data']['ret'][1]['word']
        tempId = content['data']['templateSign']
        if tempId == 'TEMPLATE_ID':

            third = "质检报告"
        else:
            third = '合格证'
        result = first + "-" + second + "-" + third
        print(result)
        return result


    except:
        print('error with {}'.format(traceback.format_exc()))


if __name__ == '__main__':
    try:
        paths = os.listdir("D:\PycharmProjects\orc\\target")
        print(paths)
        for x in paths:
            path = "D:\PycharmProjects\orc\\target\\"+x
            print(path)
            at = get_access_token()

            classifierId = 1

            result = img_2_string(path, at, classifierId)
            # print(result)
            # print(path.split(".")[1])

            result_name = "D:\PycharmProjects\orc\\result\\"+result.replace(":","")+"."+path.split(".")[1]
            # print(result_name)
            os.rename(path,result_name)
            print("{}修改完毕".format(result_name))
    except Exception as e:
        print(e)
