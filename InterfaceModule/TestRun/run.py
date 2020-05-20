"""
加载路径用于控制台命令执行python run.py用
"""
import sys,os
# 获得当前绝对路径
def get_path(file):
    path = os.path.abspath(os.path.join(os.getcwd(), file))
    # print("path:",path)
    return path
sys.path.append(get_path("../.."))
sys.path.append(get_path("../..")+"/venv/Lib/site-packages")



import unittest,time
from InterfaceModule.Dependency.BeautiifulReport.BeautifulReport import BeautifulReport
from InterfaceModule.TestCase.mokeCase.TestsmokeForDNS import mokeDnsCasesObj

# 执行全部Case
def report_data():
    print("----------------------------------------------")
    # 定义测试报告文件格式
    # testunit = unittest.TestSuite()    # 创建测试套件
    test_dir = get_path("..")+'/TestCase'         # 测试用例文件
    # print(test_dir)
    report_dir = get_path("..")+'/Report'          # 测试报告生成地址
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    #运行测试用例并生成测试报告
    # 加载测试用例
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='Test*.py')
    BeautifulReport(discover).report(filename='测试报告%s'%now, description='自动化用例', log_path=report_dir)

    '''
    #发送测试报告到邮件
    e = email()
    e.email_html()  #发送包含html附件
    e.email_send() #发送文件
    logging.info('完成发送测试邮件...')
    '''

# 执行指定Case
def report_data_for_one_Case(obj):
    report_dir = get_path("..")+'/Report'         # 测试报告生成地址
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    suite = unittest.TestSuite()  # 定义一个测试集合
    suite.addTest(unittest.makeSuite(obj))  # 把写的用例加进来（将TestCalc类）加进来
    run = BeautifulReport(suite)  # 实例化BeautifulReport模块
    run.report(filename='测试报告%s'%now, description='自动化用例', log_path=report_dir)

report_data()
# report_data_for_one_Case(mokeDnsCasesObj)
