import requests, json,threading
from InterfaceModule.Common.RequestMethod import send_method
import logging



class get_info(send_method):
    def __init__(self,login_phone='',header='',num='',network=''):
        self.login_phone = login_phone
        self.header = header
        self.num=num
        self.network=network


    def get_app_header(self):
        header_list = []
        if len(self.login_phone) == 11:
            phone = self.login_phone
            res = self.app_login(phone)
            if res:
                header_list.append(res)
        else:
            for i in range(self.num):
                if i <= 9:
                    phone = self.login_phone + '00' + str(i)
                elif i >= 10 and i <= 99:
                    phone = self.login_phone + '0' + str(i)
                elif i >= 100 and i <= 999:
                    phone = self.login_phone + str(i)
                res = self.app_login(phone)
                if res:
                    header_list.append(res)
        return header_list

    def app_login(self,phone):
        # 获取商品信息
        header = []
        if self.network=='test':
            url = 'http://test-api.wujinpu.cn/api/user/quick-login'
        elif self.network=='pre':
            url = 'https://pre-api.wujinpu.cn/api/user/quick-login'

        data={
            "code":"888888",
            "mobile":"",
            "type":"0"
        }
        data['mobile'] = phone
        response = self.send_post(url,data,response_type='',header=self.header)
        try:
            header = 'Bearer '+response['data']['access_token']
        except Exception:
            logging.info('登录异常，登录账号：%s，登录结果：%s' %(phone,response))
        return header

    def web_login(self):
        if self.network=='test':
            url = 'http://test-api.wujinpu.cn/api/user/login'
        elif self.network=='pre':
            url = 'https://pre-api.wujinpu.cn/api/user/login'

        data={
            'userType':'1',
            'mobile':'',
            'code':'888888'
        }
        data['mobile']=self.login_phone
        response = self.send_post(url, data, response_type='', header=self.header)
        try:
            header = 'Bearer '+response['data']['access_token']
        except Exception:
            logging.info('登录异常，登录账号：%s，登录结果：%s' % (self.login_phone, response))
        return header


def run_get_header(login_phone='18900003',num=1,network='test',running_work='app'):
    '''
    :param login_phone: 电话号码，输入8位数或11位数，输入11位数时，默认单登录
    :param num:  登录账号个数
    :param network:  运行环境，test/pre
    :param running_work:  工作环境：web/app，web只支持单登录
    :return: app以列表形式返回，web已字符串形式返回
    '''
    i = get_info(login_phone=login_phone, num=num,network=network)
    if running_work=='app':
        header_list = i.get_app_header()
        logging.info('获得app端：header数量:%s个，header_list内容：%s' % (len(header_list), header_list))
        return header_list
    elif running_work=='web':
        header = i.web_login()
        logging.info('获取web端：header内容：%s' % (header))
        return header


if __name__ == '__main__':
    run_get_header(login_phone='18900000001',network='test',running_work='web')