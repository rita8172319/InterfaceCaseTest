import unittest, logging, time
import logging.config
import unittest


# 启动与日志配置文件
# 日志配置
CON_LOG = '../Config/log.conf'
logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


class StartEnd(unittest.TestCase):
    '''
    def setUp(self):
        # 初始化
        logging.info("-----setUp-----")
        pass

    def tearDown(self):
        logging.info("-----tearDown-----")
        pass

    '''

    # 测试初始化(全部用例执行完成后执行)
    @classmethod
    def setUpClass(self):
        # 初始化
        logging.info("----------用例执行初始化----------")





    # 测试环境还原(全部用例执行完成后执行)
    @classmethod
    def tearDownClass(self):
        logging.info("----------用例执行结束----------")



if __name__ == '__main__':
    unittest.main()
