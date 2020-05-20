import requests, json
import logging.config
# import logging
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR=BASE_DIR.replace('\\','/')
# CON_LOG='%s/config/log.conf'%BASE_DIR
#
# print('获取TestTool层级的绝对路径：',BASE_DIR)
# logging.config.fileConfig(CON_LOG)
# logging=logging.getLogger()

class send_method(object):
    # post方法
    def send_post(self, url, data='', response_type='', header=''):
        if response_type == 'json':
            header["Content-Type"] = "application/json"
            res = requests.post(url=url, data=json.dumps(data), headers=header, verify=False)
        else:
            res = requests.post(url=url, data=data, headers=header, verify=False)
        t = json.loads(res.text)
        return t

    # get方法
    def send_get(self, url, header=''):
        res = requests.get(url=url, headers=header, verify=False)
        t = json.loads(res.text)
        return t

    # put方法
    def send_put(self, url, data='', response_type='', header=''):
        if response_type == 'json':
            header["Content-Type"] = "application/json"
            res = requests.put(url=url, data=json.dumps(data), headers=header, verify=False)
        else:
            res = requests.put(url=url, data=data, headers=header, verify=False)
        logging.info("修改结果：%s"%res)
        logging.info("修改结果：%s"%res.text)
        t = json.loads(res.text)
        return t

    # del方法
    def send_del(self, url, data='', response_type='', header=''):
        logging.info(url)
        if response_type == 'json':
            header["Content-Type"] = "application/json"
            res = requests.delete(url=url, data=json.dumps(data), headers=header, verify=False)
        else:
            res = requests.delete(url=url, headers=header, verify=False)
        # logging.info('!!!!!!!!!!:%s'%res)
        # logging.info('!!!!!!!!!!:%s'%res.text)
        if res.text!='':
            t = json.loads(res.text)
        else:
            t = res
        return t

    def send_cookie_post(self, url, cookie_data, data):
        header={}
        header["Content-Type"] = "application/json"
        res = requests.post(url=url,data=json.dumps(data), cookies=cookie_data, verify=False,headers=header)
        t = json.loads(res.text)
        return t