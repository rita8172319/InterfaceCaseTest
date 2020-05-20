import logging
from InterfaceModule.Common.Myunit import StartEnd
from InterfaceModule.Interface.UserInfoController.UserInfo import UserInfoInterface
import unittest

class GoodsShow(StartEnd):
    UserInfoInterface = UserInfoInterface()

    @unittest.skip("不执行")
    def testLoginTest1(self):
        """
        成功登陆的用例
        :return:
        """
        logging.info("------------------GoodsShow用例编号：test1------------------")
        res=self.UserInfoInterface.login(username="admin",password="admin")
        logging.info(res["code"])
        self.assertEqual(res["code"],"000")






if __name__ == '__main__':
    pass
