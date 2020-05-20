import logging
from InterfaceModule.Common.RequestMethod import send_method
import yaml


# 功能相关公共方法
class UserInfoInterface(object):
    def __init__(self):
        self.sendMethod = send_method()
        file = open('../Config/urlPath.yaml', 'r')
        self.data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
    # ----------------------------------接口信息----------------------------------
    def login(self,username,password):
        # logging.info('登录账号：%s，登录密码：%s' % (username,password))
        url = '%s/apis/linkingthing.com/example/v1/login'%self.data["urlPath"]
        data = {}
        data['username'] = username
        data['password'] = password

        # 运行
        res = self.sendMethod.send_post(url=url, data=data)
        # print(res)
        return res


if __name__ == '__main__':
    u=UserInfoInterface()
    u.login("admin","admin")
