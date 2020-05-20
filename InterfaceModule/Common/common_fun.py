import logging.config
import re,requests
import os,time,csv,yaml,random,xlsxwriter,xlrd,json,ast
from xlutils.copy import copy
import execjs
import os

# 公共模块
# class Common(object):
#     #获取当前时间
#     def getTime(self):
#         self.now = time.strftime("%Y-%m-%d %H_%M_%S")
#         return self.now
#
#     # xls中写入用例结果
#     def xls_info(self,expect,result,module,case_num,row_xls_file_name,res):
#         logging.info('common/common_fun获取预期结果expect:%s,获取实际结果result：%s'%(expect,result))
#         logging.info('common/common_fun获取res：%s'%res)
#         error_info = '用例执行编号：%s,返回信息：%s'%(case_num,res)
#         time = self.getTime()
#         xls_path = os.path.dirname(os.path.dirname(__file__)) + '/report/%s' % time.split(' ')[0]
#         logging.info('common/common_fun开始判断错误信息存放目录是否存在...')
#         # 当xls_path目录不存在时，创建目录，目录名称按每日日期算
#         if os.path.exists(xls_path):
#             pass
#         else:
#             logging.info('common/common_fun错误信息存放对应目录不存在，开始创建目录...')
#             os.mkdir(xls_path)
#             logging.info('common/common_fun创建report-%s文件夹'%time.split(' ')[0])
#
#         # 获取错误信息xls文件名
#         xls_file = xls_path + '/%s%s.xls' % (module,time.split(' ')[0])
#         xls_file = xls_file.replace('\\','/')
#         logging.info('common/common_fun获取xls文件路径：%s'%xls_file)
#
#         # 获取原始用例文件（用于错误信息存储复制）
#         row_xls_file = os.path.dirname(os.path.dirname(__file__)) + '/config/%s' %row_xls_file_name
#         # 当xls_file文件不存在时，创建目录，目录名称按每日日期算
#         if os.path.exists(xls_file):
#             logging.info('common/common_fun错误信息文件存在，开始存入文件...')
#             # xls_file文件存在，读取目录（copy），并写入错误
#             rb = xlrd.open_workbook(xls_file)
#             xl = copy(rb)
#             # 获取sheet对象，通过sheet_by_index()获取的sheet对象没有write()方法
#             ws = xl.get_sheet(0)
#             # 获取当前xls最大行数
#             row_num = self.xls_info_num(xls_file)
#             logging.info('common/common_fun获取获取当前xls最大行数：%s行'%row_num)
#             # 写入数据
#             # res为请求返回数据，包含"res_code"，1表示成功，0表示失败
#             if expect == result:
#                 data = '请求成功:'+error_info
#
#                 # 当获取大数据文件时
#                 if len(data)>=32767:
#                     logging.info('common/common_fun获取数据大于32767，进行1：10切片')
#                     dataArr = re.findall('.{' + str(10) + '}', data)
#                     dataArr.append(data[(len(dataArr) * 1):])
#                     datainfo = str(dataArr[0:10])
#                     ws.write(case_num, 10, datainfo)
#                 else:
#                     ws.write(case_num, 10, data)
#             else:
#                 data = '请求失败:' + error_info
#                 # 当获取大数据文件时
#                 if len(data) >= 32767:
#                     logging.info('common/common_fun获取数据大于32767，进行1：10切片')
#                     dataArr = re.findall('.{' + str(10) + '}', data)
#                     dataArr.append(data[(len(dataArr) * 1):])
#                     datainfo = str(dataArr[0:10])
#                     ws.write(case_num, 10, datainfo)
#                 else:
#                     ws.write(case_num, 10, data)
#
#             # 添加sheet页
#             # wb.add_sheet('sheetnnn2',cell_overwrite_ok=True)
#             # 利用保存时同名覆盖达到修改excel文件的目的,注意未被修改的内容保持不变
#             xl.save(xls_file)
#
#         else:
#             # xls_file文件不存在，复制原始目录,并写入错误
#             logging.info('common/common_fun错误信息文件不存在，开始生成（复制）用例报告文件...')
#             rb = xlrd.open_workbook(row_xls_file)
#             xl = copy(rb)
#             # 获取sheet对象
#             ws = xl.get_sheet(0)
#             # 实际结果与预期结果不相等时，写入内容
#             if expect == result:
#                 data = '请求成功:'+error_info
#                 # 当获取大数据文件时
#                 if len(data) >= 32767:
#                     logging.info('common/common_fun获取数据大于32767，进行1：10切片')
#                     dataArr = re.findall('.{' + str(10) + '}', data)
#                     dataArr.append(data[(len(dataArr) * 1):])
#                     datainfo = str(dataArr[0:10])
#                     ws.write(case_num, 10, datainfo)
#                 else:
#                     ws.write(case_num, 10, data)
#
#             else:
#                 data = '请求失败:' + error_info
#                 # 当获取大数据文件时
#                 if len(data) >= 32767:
#                     logging.info('common/common_fun获取数据大于32767，进行1：10切片')
#                     dataArr = re.findall('.{' + str(10) + '}', data)
#                     dataArr.append(data[(len(dataArr) * 1):])
#                     datainfo = str(dataArr[0:10])
#                     ws.write(case_num, 10, datainfo)
#                 else:
#                     ws.write(case_num, 10, data)
#
#             xl.save(xls_file)
#
#     # 获取当前xls文件最大行数
#     def xls_info_num(self,xls_file):
#         xl = xlrd.open_workbook(xls_file) #打开excel
#         table = xl.sheets()[0]   #通过索引获取工作表
#         row_num = 0  # 预置行数
#         while 1:
#             try:
#                 if table.row_values(row_num):
#                     row_num = row_num + 1
#             except Exception:
#                 break
#         logging.info('common/common_fun获取到当前xls文件最大行数：%s'%row_num)  # 实际行数
#         return row_num
#
#     # 获取csv文件内容（存储用户信息）
#     def get_csv_data(self,line,csv_name):
#         '''
#         :param csv_file: csv文件路径
#         :param line: 数据行数
#         '''
#         csv_path = '../data/%s'%csv_name
#         with open(csv_path, 'r', encoding='utf-8-sig') as file:
#             reader = csv.reader(file)
#             for index, row in enumerate(reader, 1):
#                 if index == line:
#                     logging.info('common/common_fun获取csv参数 %s ' % row)
#                     return row
#
#     # 随机生成5位数
#     def v_code(self):
#         code = ''
#         for i in range(5):
#             num = random.randint(0, 9)
#             alf = chr(random.randint(65, 90))
#             add = random.choice([num, alf])
#             code += str(add)
#         return code
#
#     # 请求方法
#     def send_post(self, url, data, response_type='', header=''):
#         # logging.info('post请求获取url：%s'%url)
#         # logging.info('post请求获取data：%s'%data)
#         # logging.info('post请求获取header：%s'%header)
#
#         if response_type == 'json':
#             header["Content-Type"] = "application/json"
#             res = requests.post(url=url, data=json.dumps(data), headers=header, verify=False)
#         else:
#             res = requests.post(url=url, data=data, headers=header, verify=False)
#         t = json.loads(res.text)
#         return t
#
#     def send_get(self, url, header=''):
#         res = requests.get(url=url, headers=header, verify=False)
#         t = json.loads(res.text)
#         return t
#
#     def send_cookie_post(self, url,cookie_data, data):
#         res = requests.post(url=url, data=data,cookies=cookie_data, verify=False)
#         # print(res.text)
#         t = json.loads(res.text)
#         return t
#
# # excel相关公共模块
# class excel_common(object):
#     # 需要输入对应excel文件名
#     def __init__(self,excel_name,sheet_id=0):
#         self.csv_path = '../config/%s' % excel_name
#         self.sheet_id = sheet_id
#         self.table = self.get_excel_table() # 获取excel文件table
#
#     # 获取excel文件table
#     def get_excel_table(self):
#         # 打开data
#         data = xlrd.open_workbook(self.csv_path)
#         # 选择页面
#         table = data.sheets()[self.sheet_id]
#         return table
#
#     # 获取单元格行数
#     def get_line(self):
#         table = self.table
#         return table.nrows
#
#     # 获取单个单元格内容
#     def get_cell_value(self,row,col):
#         # row:行,col:列
#         return self.table.cell_value(row,col)
#
# # json相关公共模块
# class json_common(object):
#
#     def __init__(self,json_name):
#         self.json_name=json_name
#         self.data=self.interface_json_info()
#
#     # 获取全部json数据
#     def interface_json_info(self):
#         with open('../data/%s' % self.json_name) as fp:
#             data = json.load(fp)
#             return data
#
#     # 通过关键字获取数据
#     def get_data(self,json_key_word):
#         return self.data[json_key_word]

class Common(object):
    # 获取绝对路径
    def get_JSpath(self,JSName):
        test_dir = "../.." + '/InterfaceModule/Common/JSFile/%s'%JSName
        path = os.path.abspath(os.path.join(os.getcwd(), test_dir))
        return path
    # 加载js文件
    def get_js(self,jsPath):
        f = open(jsPath, 'r', encoding='utf-8')  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr
    # 加载js函数
    def get_des_psswd(self,jsPath, funcName, parameter):
        js_str = self.get_js(jsPath)
        ctx = execjs.compile(js_str)  # 加载JS文件
        return (ctx.call(funcName, parameter))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数




if __name__ == '__main__':
    '''
    # UI自动化
    # 继承基类：desired_caps.py——browser_desired()，打开浏览器并跳转网页
    driver = browser_desired('chrome')
    # 获取实例
    c=Common(driver)
    # 截图
    c.getScreenShot('测试模块')
    # 获取时间
    print(c.getTime())
    # 获取csv文件内容,第一列
    data = c.get_csv_data(1)
    print(data)
    # 获取五位数随机元素
    print(c.v_code())
    '''


    # excel
    # e = excel_common('all.xls')
    # print(e.get_line())
    # print(e.get_cell_value(1,0))



    # json
    # j=json_common('all_interface.json')
    # print(j.interface_json_info())

