import logging
import unittest
import yaml
import time
from datetime import datetime
from InterfaceModule.Common.Myunit import StartEnd
from InterfaceModule.Interface.DnsInterface.DnsInterface import DnsInterfaceObj
from InterfaceModule.Common.RequestMethod import send_method
from InterfaceModule.Business.DnsBusiness import DnsBusinessObj
from InterfaceModule.Interface.UserInfoController.UserInfo import UserInfoInterface


class mokeDnsCasesObj(StartEnd):
    def __init__(self, *args, **kwargs):
        super(mokeDnsCasesObj, self).__init__(*args, **kwargs)
        # DNS用例接口类
        self.obj = DnsInterfaceObj()
        # DNS业务类
        self.dbo = DnsBusinessObj()

        # 获取登录token，并生成header
        u = UserInfoInterface()
        res = u.login(username="admin", password="admin")
        token = res["token"]
        self.header = {}
        self.header['Authorization'] = "Bearer %s" % token

        # 获取yaml配置文件
        urlPathYamlFile = open('../Config/urlPath.yaml', 'r', encoding='utf-8')
        self.urlPathYaml = yaml.load(urlPathYamlFile, Loader=yaml.FullLoader)

        # 获取数据请求对象
        self.sendMethod = send_method()

        # acl/view/zone/record 的名称定义
        self.urlPath = self.urlPathYaml["urlPath"]
        # 全部域名相同的情况
        self.zoneSameName = "zone.com"
        self.recordSameName = "mail"
        # 第一套视图用
        self.acl01Name = "acl01"
        self.acl01Ip = "192.168.1.0/24"
        self.view01Name = "view01"
        self.record01IPV4IP = "192.1.1.1"
        self.record01IPV6IP = "2001:DB8:2de::e13"
        self.record01TTL = 200
        # 第二套视图用
        self.acl02Name = "acl02"
        self.acl02Ip = "192.168.0.0/24"
        self.view02Name = "view02"
        self.record02IPV4IP = "192.2.2.2"
        self.record02IPV6IP = "2001::e13"
        self.record02TTL = 200
        # 默认视图用
        self.recordForDefaultIPV4IP = "192.6.6.6"
        self.recordForDefaultIPV6IP = "2001::e66"
        self.recordForDefaultTTL = 200
        # 修改用
        self.modifyAcl01Ip = "192.168.2.0/24"
        self.modifyAclName = "acl"
        self.delAclName = "delAcl"
        self.modifyRecord01IPV4IP = "192.1.1.2"
        self.modifyRecord01IPV6IP = "1::2"
        self.modifyRecord01TTL = 200
        # 重定向用
        # 间接默认视图用
        self.recordForRedirectionsIPV4IP = "192.3.3.3"
        self.recordForRedirectionsIPV6IP = "2223::"
        self.recordForRedirectionsTTL = 200
        # 直接默认视图用
        self.recordForRedirectionsRpzIPV4IP = "192.5.5.5"
        self.recordForRedirectionsRpzIPV6IP = "2001:2e::55"
        self.recordForRedirectionsRpzTTL = 200

        # 关闭yaml连接
        urlPathYamlFile.close()

    '''
    1.由一个地址访问一个视图
    2.解析视图中IPV4与IPV6的资源记录。
    '''

    @unittest.skip("不执行")
    def test_A0_addAcl(self):
        """
        测试内容：
            新建访问控制
        测试步骤：
            1.新建一个名称为self.acl01Name的访问控制列表，IP为：self.record01IPV4IP
        预期结果：新建成功
        """
        logging.info("------------------mokeForDNS用例编号：A0------------------")
        data = {}
        data['list'] = [{"check": "false", "name": self.acl01Ip, "aclid": "1", "type": "ip"}]
        data['name'] = self.acl01Name
        res = self.obj.aclsInterface(url=self.urlPath, method="post", data=data, header=self.header)
        # 判断新创建的名称是否为self.acl01Name
        self.assertEqual(res['name'], self.acl01Name)

    @unittest.skip("不执行")
    def test_A1_getAcl(self):
        """
        测试内容：
            查看访问控制列表名称/IP
        测试步骤：
            1.查询名称self.acl01Name对应的记录，名称、IP是否正确
        预期结果：访问控制的名称为self.acl01Name，IP为：self.acl01Ip
        """
        logging.info("------------------mokeForDNS用例编号：A1------------------")
        res = self.obj.aclsInterface(url=self.urlPath, method="get", header=self.header)
        # 判断名称是否包含self.acl01Name，其IP是否为：self.acl01Ip
        aclIp = ''
        for i in res['data']:
            if i['name'] == self.acl01Name:
                logging.info(i)
                logging.info(i["list"][0]["name"])
                aclIp = i["list"][0]["name"]
        self.assertEqual(aclIp, self.acl01Ip)

    @unittest.skip("不执行")
    def test_A2_getAcl(self):
        """
        测试内容：
            查看访问控制列表创建时间
        测试步骤：
            1.进入访问控制列表，查询名称【acl01】对应的时间是否正确
        预期结果：acl01的时间在当前时间5分钟以内
        """
        logging.info("------------------mokeForDNS用例编号：A2------------------")
        res = self.obj.aclsInterface(url=self.urlPath, method="get", header=self.header)

        # 判断名称是否包含self.acl01Name，并获取其创建时间
        strtime = '2020-01-01 00:00:00'
        for i in res['data']:
            if i['name'] == self.acl01Name:
                logging.info(i)
                logging.info(i["creationTimestamp"])
                strtime = i["creationTimestamp"]
        # 获取acl创建的时间戳
        strtime = strtime.replace('Z', '')
        strtime = strtime.replace('T', ' ')
        strtime = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
        tstamp = strtime.timestamp()
        # 获取当前时间戳
        timeNow = time.time()

        # 判断时间是否在当前时间5分钟范围内
        state = "false"
        if int(tstamp) < int(timeNow) and int(tstamp) > int(timeNow - 300):
            state = "true"
        self.assertEqual(state, "true")

    # @unittest.skip("不执行")
    def test_A3_addView(self):
        """
        测试内容：
            新建视图
        测试步骤：
            1.获取aclId
            2.新建一个名称为self.view01Name的视图，访问控制列表选择self.acl01Name，优先级为1
        预期结果：新建成功
        """
        logging.info("------------------mokeForDNS用例编号：A3------------------")
        res = self.dbo.addViewCommon(aclName=self.acl01Name, viewName=self.view01Name, url=self.urlPath,
                                     header=self.header)
        logging.info(res['name'])
        self.assertEqual(res['name'], self.view01Name)

    @unittest.skip("不执行")
    def test_A4_getView(self):
        """
        测试内容：
            查询视图
        测试步骤：
            1.进入视图管理页面，查询名称self.view01Name对应的记录，名称、访问控制列表、优先级是否正确
        预期结果：可见视图名称为self.view01Name，访问控制为：self.acl01Name，优先级为1
        """
        logging.info("------------------mokeForDNS用例编号：A4------------------")
        # 获取视图信息
        res = self.obj.viewsInterface(url=self.urlPath, method="get", header=self.header)
        # 判断是否存在self.view01Name的视图，优先级是否为1
        state = "false"
        for i in res["data"]:
            if i['name'] == self.view01Name:
                logging.info(i)
                if i['priority'] == 1:
                    state = "true"
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_A5_AddZone(self):
        """
        测试内容：
            新建区域
        测试步骤：
            1.获取视图self.view01Name的id
            2.新建区域self.zoneSameName
        预期结果：创建成功
        """
        logging.info("------------------mokeForDNS用例编号：A5------------------")
        res = self.dbo.addZoneCommon(viewName=self.view01Name, zoneName=self.zoneSameName, url=self.urlPath,
                                     header=self.header)
        logging.info("获取新建的区域名称：%s" % res['name'])
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_A6_getZone(self):
        """
        测试内容：
            查询区域
        测试步骤：
            1.进入权威管理页面-视图self.view01Name
            2.查询区域self.zoneSameName
        预期结果：可见当前页面的区名称self.zoneSameName资源记录数量为0
        """
        logging.info("------------------mokeForDNS用例编号：A6------------------")
        # 获取视图id
        res = self.obj.viewsInterface(url=self.urlPath, method="get", header=self.header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == self.view01Name:
                logging.info(i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)
        # 获取区域信息
        res = self.obj.zonesInterface(url=self.urlPath, method="get", viewId=viewId, header=self.header)
        state = "false"
        for i in res['data']:
            logging.info("获取区域名称：%s" % i['name'])
            if i['name'] == self.zoneSameName:
                if i['rrsize'] == 0:
                    state = "true"
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_A7_AddRecordForIPV4(self):
        """
        测试内容：
            新建ipv4资源记录
        测试步骤：
        1.进入权威管理页面-视图view01Name-区域self.zoneSameName并进入到资源记录页面
        2.新建资源记录，名称为self.recordSameName选择类型A，填写记录值self.record01IPV4IP，TTL：self.record01TTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：A7------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view01Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record01IPV4IP, recordTTL=self.record01TTL, recordType="A",
                                       url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_A8_AddRecordForIPV6(self):
        """
        测试内容：
            新建ipv6资源记录
        测试步骤：
        1.进入权威管理页面-视图view01Name-区域self.zoneSameName并进入到资源记录页面
        2.新建资源记录，名称为self.recordSameName选择类型AAAA，填写记录值record01IPV6IP，TTL：self.record01TTL
        预期结果：1.ipv6地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：A8------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view01Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record01IPV6IP, recordTTL=self.record01TTL, recordType="AAAA",
                                       url=self.urlPath, header=self.header)

        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_A9_analysisRecordForIPV4(self):
        """
        测试内容：
            解析ipv4资源记录
        测试步骤：
        1.1.在terminal01Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：1.返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：A9------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"],
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_B0_analysisRecordForIPV6(self):
        """
        测试内容：
            解析ipv6资源记录
        测试步骤：
        1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：1.返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：B0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    '''
    1.由两个不同的地址，访问两个不同的视图
    2.解析视图中IPV4与IPV6的资源记录。
    '''

    @unittest.skip("不执行")
    def test_B1_addAcl(self):
        """
        测试内容：
            新建访问控制2
        测试步骤：
        1.进入访问控制列表页面，新建一个名称为self.acl02Name的访问控制列表，IP为：self.acl02Ip
        预期结果：新建成功
        """
        logging.info("------------------mokeForDNS用例编号：B1------------------")
        data = {}
        data['list'] = [{"check": "false", "name": self.acl02Ip, "aclid": "1", "type": "ip"}]
        data['name'] = self.acl02Name
        # 运行
        res = self.obj.aclsInterface(url=self.urlPath, method="post", data=data, header=self.header)
        logging.info("新建acl返回值res:%s" % res)
        self.assertEqual(res['name'], self.acl02Name)

    @unittest.skip("不执行")
    def test_B2_addView(self):
        """
        测试内容：
            新建视图2
        测试步骤：
        1.获取acl02Id
        2.新建一个名称为self.view02Name的视图，访问控制列表选择self.acl02Name，优先级为1
        预期结果：新建成功
        """
        logging.info("------------------mokeForDNS用例编号：B2------------------")
        res = self.dbo.addViewCommon(aclName=self.acl02Name, viewName=self.view02Name, url=self.urlPath,
                                     header=self.header)
        logging.info(res['name'])
        self.assertEqual(res['name'], self.view02Name)

    @unittest.skip("不执行")
    def test_B3_getView(self):
        """
        测试内容：
            查询视图2
        测试步骤：
        1.进入视图管理页面，查询名称self.view02Name对应的记录，名称、访问控制列表、优先级是否正确
        预期结果：1.可见视图名称为self.view02Name，访问控制为：self.acl02Name，优先级为1，self.view01Name优先级不为1
        """
        logging.info("------------------mokeForDNS用例编号：B3------------------")
        # 获取视图信息
        res = self.obj.viewsInterface(url=self.urlPath, method="get", header=self.header)

        # 判断是否存在self.view02Name的视图，优先级是否为1
        stateA = "false"
        for i in res["data"]:
            if i['name'] == self.view02Name:
                logging.info(i)
                if i['priority'] == 1:
                    stateA = "true"

        # 判断是否存在self.view01Name的视图，优先级是否不为1
        stateB = "false"
        for i in res["data"]:
            if i['name'] == self.view01Name:
                logging.info(i)
                if i['priority'] != 1:
                    stateB = "true"

        self.assertEqual(stateA and stateB, "true")

    @unittest.skip("不执行")
    def test_B4_AddZone(self):
        """
        测试内容：
            新建视图2的区域
        测试步骤：
            1.获取视图self.view02Name的id
            2.新建区域self.zoneSameName
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：B4------------------")
        res = self.dbo.addZoneCommon(zoneName=self.zoneSameName, viewName=self.view02Name, url=self.urlPath,
                                     header=self.header)
        logging.info("获取新建的区域名称：%s" % res['name'])
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_B5_AddRecordForIPV4(self):
        """
        测试内容：
            新建视图2的IPV4记录
        测试步骤：
            1.进入权威管理页面-视图view02Name-区域zone02Name并进入到资源记录页面
            2.新建资源记录，名称为record02Name选择类型A，填写记录值record02IPV4IP，TTL：self.record02TTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：B5------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view02Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record02IPV4IP, recordTTL=self.record02TTL, recordType="A",
                                       url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_B6_AddRecordForIPV6(self):
        """
        测试内容：
            新建视图2的IPV6记录
        测试步骤：
        1.进入权威管理页面-视图view02Name-区域zone02Name并进入到资源记录页面
        2.新建资源记录，名称为record02Name选择类型AAAA，填写记录值record02IPV6IP，TTL：self.record02TTL
        预期结果：1.ipv6地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：B6------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view02Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record02IPV6IP, recordTTL=self.record02TTL, recordType="AAAA",
                                       url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_B7_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal01Server解析域名ipv4地址
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：B7------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_B8_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal01Server解析域名ipv6地址
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：B8------------------")
        # 获取终端连接
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_B9_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal02Server解析域名ipv4地址
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record02IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：B9------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.record02IPV4IP,
            recordTTL=self.record02TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_C0_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal02Server解析域名ipv6地址
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record02IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：C0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.record02IPV6IP,
            recordTTL=self.record02TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    '''
    1.通过可以访问的域名,访问默认视图
    '''

    @unittest.skip("不执行")
    def test_C1_AddZoneForDefault(self):
        """
        测试内容：
            新建默认视图区域
        测试步骤：
            1.获取视图default的id
            2.新建区域self.zoneSameName
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：C1------------------")
        res = self.dbo.addZoneCommon(zoneName=self.zoneSameName, viewName='default', url=self.urlPath,
                                     header=self.header)
        logging.info("获取新建的区域名称：%s" % res['name'])
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_C2_AddRecordIPV4ForDefault(self):
        """
        测试内容：
            新建默认视图区域IPV4记录
        测试步骤：
            1.进入权威管理页面-视图default-区域zoneSameName并进入到资源记录页面
            2.新建资源记录，名称为recordSameName选择类型A，填写记录值recordForDefaultIPV4IP，TTL：recordForDefaultTTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：C2------------------")
        res = self.dbo.AddRecordCommon(viewName="default", zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.recordForDefaultIPV4IP, recordTTL=self.recordForDefaultTTL,
                                       recordType="A", url=self.urlPath, header=self.header)

        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_C3_AddRecordIPV6ForDefault(self):
        """
        测试内容：
            新建默认视图区域IPV6记录
        测试步骤：
            1.进入权威管理页面-视图default-区域zoneSameName并进入到资源记录页面
            2.新建资源记录，名称为recordSameName选择类型AAAA，填写记录值recordForDefaultIPV6IP，TTL：recordForDefaultTTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：C3------------------")
        res = self.dbo.AddRecordCommon(viewName="default", zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.recordForDefaultIPV6IP, recordTTL=self.recordForDefaultTTL,
                                       recordType="AAAA", url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_C4_defaultAnalysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，由于可以访问到对应的地址，不能访问到默认视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：C4------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_C5_defaultAnalysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，由于可以访问到对应的地址，不能访问到默认视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：C5------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    '''
    1.acl修改、删除、嵌套
    2.通过不能解析的域名访问默认视图
    '''

    @unittest.skip("不执行")
    def test_C6_modifyAcl(self):
        """
        测试内容：
            修改acl的测试访问IP，为非测试访问IP
        测试步骤：
            1.进入访问控制列表页面，编辑【self.acl01Name】，修改IP为：self.modifyIp
        预期结果：新建成功，IP变为self.modifyIp，创建时间不变
        """
        logging.info("------------------mokeForDNS用例编号：C6------------------")
        state = self.dbo.modifyAclCommon(aclName=self.acl01Name, modifyAclIp=self.modifyAcl01Ip, url=self.urlPath,
                                         header=self.header)
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_C7_defaultAnalysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，由于不能访问到对应的地址，所以可以访问default视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：C7------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.recordForDefaultIPV4IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_C8_defaultAnalysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，由于不能访问到对应的地址，所以可以访问default视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：C8------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.recordForDefaultIPV6IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_C9_modifyAclIP(self):
        """
        测试内容：
            修改acl的非测试访问IP，为测试访问IP
        测试步骤：
            1.编辑【self.acl01Name】的访问控制列表，IP为：self.acl01Ip
        预期结果：新建成功，IP变为self.acl01Ip，创建时间不变
        """
        logging.info("------------------mokeForDNS用例编号：C9------------------")
        state = self.dbo.modifyAclCommon(aclName=self.acl01Name, modifyAclIp=self.acl01Ip, url=self.urlPath,
                                         header=self.header)
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_D0_defaultAnalysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，由于能访问到对应的地址，所以会访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：D0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_D1_defaultAnalysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，由于能访问到对应的地址，所以会访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer01 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：D1------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_D2_modifyAclName(self):
        """
        测试内容：
            修改acl名称
        测试步骤：
            1.编辑【self.acl01Name】的访问控制列表，名称改为self.modifyAclName
        预期结果：新建成功，名称变为self.modifyAclName，创建时间不变
        """
        logging.info("------------------mokeForDNS用例编号：D2------------------")
        state = self.dbo.modifyAclCommon(aclName=self.acl01Name, modifyAclIp=self.acl01Ip,
                                         modifyAclName=self.modifyAclName, url=self.urlPath, header=self.header)
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_D3_getView(self):
        """
        测试内容：
            查询acl名称
        测试步骤：
            1.查询视图名称self.view01Name对应的记录，名称、访问控制列表、优先级是否正确
        预期结果：可见视图名称为self.view01Name，访问控制为：self.modifyAclName，优先级为2
        """
        logging.info("------------------mokeForDNS用例编号：D3------------------")
        # 获取视图信息
        res = self.obj.viewsInterface(url=self.urlPath, method="get", header=self.header)
        # 判断是否存在self.view01Name的视图，优先级是否为2
        state = "false"
        for i in res["data"]:
            if i['name'] == self.view01Name:
                logging.info(i)
                if i['priority'] == 2 and i['acls'][0]['name'] == self.modifyAclName:
                    state = "true"
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_D4_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：D4------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_D5_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：D5------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_D6_delAcl(self):
        """
        测试内容：
            删除使用中acl：self.acl02Name
        测试步骤：
        预期结果：删除失败
        """
        logging.info("------------------mokeForDNS用例编号：D6------------------")
        res = self.dbo.delAclCommon(aclName=self.acl02Name, url=self.urlPath, header=self.header)
        logging.info(res)
        self.assertEqual(res['status'], 400)

    @unittest.skip("不执行")
    def test_D7_addAcl(self):
        """
        测试内容：
            新建的acl
        测试步骤：
            1.进入访问控制列表页面，新建一个名称为self.delAclName的访问控制列表，IP为：1.1.1.0/24
        预期结果：新建成功
        """
        logging.info("------------------mokeForDNS用例编号：D7------------------")
        data = {}
        data['list'] = [{"check": "false", "name": "1.1.1.0/24", "aclid": "1", "type": "ip"}]
        data['name'] = self.delAclName
        res = self.obj.aclsInterface(url=self.urlPath, method="post", data=data, header=self.header)
        # 判断新创建的名称是否为self.acl01Name
        self.assertEqual(res['name'], self.delAclName)

    @unittest.skip("不执行")
    def test_D8_delAcl(self):
        """
        测试内容：
            删除未使用的acl:self.delAclName
        测试步骤：
        预期结果：删除失败
        """
        logging.info("------------------mokeForDNS用例编号：D8------------------")
        res = self.dbo.delAclCommon(aclName=self.delAclName, url=self.urlPath, header=self.header)
        logging.info("删除结果：%s" % res)
        # 查询是否还存在self.delAclName
        res = self.obj.aclsInterface(url=self.urlPath, method="get", header=self.header)
        # 判断名称是否包含self.delAclName
        state = "true"
        for i in res['data']:
            if i['name'] == self.delAclName:
                state = "false"
        self.assertEqual(state, "true")

    '''
    视图修改、删除
    '''

    @unittest.skip("不执行")
    def test_D9_delView(self):
        """
        测试内容：
            1.删除self.view02Name视图
        测试步骤：
        预期结果：1.删除成功，当前页面不再有self.view02Name视图
        """
        logging.info("------------------mokeForDNS用例编号：D9------------------")
        # 删除视图
        res = self.dbo.delViewCommon(viewName=self.view02Name, url=self.urlPath, header=self.header)
        logging.info("删除结果：%s" % res)
        # 查询是否还存在self.view02Name
        res = self.obj.viewsInterface(url=self.urlPath, method="get", header=self.header)
        # 判断名称是否包含self.view02Name
        state = "true"
        for i in res['data']:
            if i['name'] == self.view02Name:
                state = "false"
        self.assertEqual(state, "true")

    @unittest.skip("不执行")
    def test_E0_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E1_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，访问到view01Name视图
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E1------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E2_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv4，访问到default视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E2------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.recordForDefaultIPV4IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E3_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv6，访问到default视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E3------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.recordForDefaultIPV6IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E4_modifyView(self):
        """
        测试内容：
            修改视图【view01Name】的访问控制为【self.acl02Name】
        测试步骤：
        预期结果：1.修改成功，可见视图名称为self.view01Name，访问控制为：self.acl02Name，优先级为1
        """
        logging.info("------------------mokeForDNS用例编号：E4------------------")
        state = self.dbo.modifyViewCommon(viewName=self.view01Name, aclName=self.acl02Name, url=self.urlPath,
                                          header=self.header)
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E5_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv4，由于view01的acl改为acl02，所以访问到default视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E5------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="A",
            recordIP=self.recordForDefaultIPV4IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E6_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal01Server解析域名ipv6，由于view01的acl改为acl02，所以访问到default视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForDefaultIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E6------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal01Server"],
            terminaUsername=self.urlPathYaml["terminal01Username"],
            terminaPassword=self.urlPathYaml["terminal01Password"],
            analysisType="AAAA",
            recordIP=self.recordForDefaultIPV6IP,
            recordTTL=self.recordForDefaultTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E7_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv4，由于view01Name的acl改为acl02，所以访问到view01Name视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E7------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E8_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv6，由于view01Name的acl改为acl02，所以访问到view01Name视图
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.record01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：E8------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_E9_delZone(self):
        """
        测试内容：
            删除view01Name中的zoneSameName
        测试步骤：
            1.获取viewID-获取zoneID-删除zone
        预期结果：1.删除成功，查询是否还存在zoneSameName
        """
        logging.info("------------------mokeForDNS用例编号：E9------------------")
        state = self.dbo.delZoneCommon(self.view01Name, self.zoneSameName, url=self.urlPath, header=self.header)
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F1_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv4，由于view01的区域删除，所以无法解析任何内容，会进行递归到外网查询
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：不能解析到self.record01IPV4IP及self.recordForDefaultIPV4IP
        """
        logging.info("------------------mokeForDNS用例编号：F1------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        stateForView, list = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.record01IPV4IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"],
            isGetResList='true'
        )
        # 判断是否访问到了默认视图
        stateForIsDefalutView = 'false'
        for i in list:
            if self.recordForDefaultIPV4IP.lower() in i:
                i = i.split("\t")
                logging.info(i)
                stateForIsDefalutView = 'true'

        # 判断是否解析结果既不是self.record01IPV4IP也不是self.recordForDefaultIPV4IP
        state = 'xxx'
        if stateForView == 'false' and stateForIsDefalutView == 'false':
            state = 'true'
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F2_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal02Server解析域名ipv6，由于view01的区域删除，所以无法解析任何内容，会进行递归到外网查询
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：不能解析到self.record01IPV6IP及self.recordForDefaultIPV6IP
        """
        logging.info("------------------mokeForDNS用例编号：F2------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        stateForView, list = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.record01IPV6IP,
            recordTTL=self.record01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"],
            isGetResList='true'
        )
        # 判断是否访问到了默认视图
        stateForIsDefalutView = 'false'
        for i in list:
            if self.recordForDefaultIPV6IP.lower() in i:
                i = i.split("\t")
                logging.info(i)
                stateForIsDefalutView = 'true'

        # 判断是否解析结果既不是self.record01IPV4IP也不是self.recordForDefaultIPV4IP
        state = ''
        if stateForView == 'false' and stateForIsDefalutView == 'false':
            state = 'true'
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F3_AddZone(self):
        """
        测试内容：
            新建view01Name的区域self.zoneSameName
        测试步骤：
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：F3------------------")
        res = self.dbo.addZoneCommon(zoneName=self.zoneSameName, viewName=self.view01Name, url=self.urlPath,
                                     header=self.header)
        logging.info("获取新建的区域名称：%s" % res['name'])
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_F4_AddRecordForIPV4(self):
        """
        测试内容：
            新建ipv4资源记录
        测试步骤：
            1.进入权威管理页面-视图view01Name-区域self.zoneSameName并进入到资源记录页面
            2.新建资源记录，名称为self.recordSameName选择类型A，填写记录值self.record01IPV4IP，TTL：self.record01TTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：F4------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view01Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record01IPV4IP, recordTTL=self.record01TTL, recordType="A",
                                       url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_F5_AddRecordForIPV6(self):
        """
        测试内容：
            新建ipv6资源记录
        测试步骤：
            1.进入权威管理页面-视图view01Name-区域self.zoneSameName并进入到资源记录页面
            2.新建资源记录，名称为self.recordSameName选择类型AAAA，填写记录值self.record01IPV6IP，TTL：self.record01TTL
        预期结果：1.ipv4地址创建成功
        """
        logging.info("------------------mokeForDNS用例编号：F5------------------")
        res = self.dbo.AddRecordCommon(viewName=self.view01Name, zoneName=self.zoneSameName,
                                       recordName=self.recordSameName,
                                       recordIP=self.record01IPV6IP, recordTTL=self.record01TTL,
                                       recordType="AAAA", url=self.urlPath, header=self.header)
        logging.info("获取新建的资源名称：%s" % res['name'])
        self.assertEqual(res['name'], self.recordSameName)

    @unittest.skip("不执行")
    def test_F6_modifyRecordForIPV4(self):
        """
        测试内容：
            修改ipv4资源记录
        测试步骤：
            1.修改view01Name/zoneSameName/recordSameName/类型为A的record01IPV4IP的资源记录
            2.修改内容：名称：recordSameName记录值：modifyRecord01IPV4IP，TTL：self.modifyRecord01TTL
        预期结果：1.ipv4地址修改成功
        """
        logging.info("------------------mokeForDNS用例编号：F6------------------")
        res = self.dbo.modifyRecordCommon(
            viewName=self.view01Name,
            zoneName=self.zoneSameName,
            recordName=self.recordSameName,
            originalRecordIP=self.record01IPV4IP,
            modifyRecordIP=self.modifyRecord01IPV4IP,
            modifyRecordTTL=self.modifyRecord01TTL,
            modifyRecordType="A",
            modifyRecordName=self.recordSameName,
            url=self.urlPath,
            header=self.header
        )

        # 查询是否修改成功
        state = "false"
        if res['name'] == self.recordSameName and res['value'] == self.modifyRecord01IPV4IP:
            state = 'true'

        logging.info("获取修改的资源：%s" % res)
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F7_modifyRecordForIPV6(self):
        """
        测试内容：
            修改ipv6资源记录
        测试步骤：
            1.修改view01Name/zoneSameName/recordSameName/类型为AAAA的record01IPV6IP的资源记录
            2.修改内容：名称：recordSameName记录值：modifyRecord01IPV6IP，TTL：self.modifyRecord01TTL
        预期结果：1.ipv6地址修改成功
        """
        logging.info("------------------mokeForDNS用例编号：F7------------------")
        res = self.dbo.modifyRecordCommon(
            viewName=self.view01Name,
            zoneName=self.zoneSameName,
            recordName=self.recordSameName,
            originalRecordIP=self.record01IPV6IP,
            modifyRecordIP=self.modifyRecord01IPV6IP,
            modifyRecordTTL=self.modifyRecord01TTL,
            modifyRecordType="AAAA",
            modifyRecordName=self.recordSameName,
            url=self.urlPath,
            header=self.header
        )

        # 查询是否修改成功
        state = "false"
        if res['name'] == self.recordSameName and res['value'] == self.modifyRecord01IPV6IP:
            state = 'true'

        logging.info("获取修改的资源：%s" % res)
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F8_analysisRecordForIPV4(self):
        """
        测试内容：
            通过terminal02Server解析域名，解析修改后的ipv4记录
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：self.modifyRecord01IPV4IP
        """
        logging.info("------------------mokeForDNS用例编号：F8------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.modifyRecord01IPV4IP,
            recordTTL=self.modifyRecord01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        # 判断是否解析结果既不是self.record01IPV4IP也不是self.recordForDefaultIPV4IP
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_F9_analysisRecordForIPV6(self):
        """
        测试内容：
            通过terminal02Server解析域名，解析修改后的ipv6记录
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：self.modifyRecord01IPV6IP
        """
        logging.info("------------------mokeForDNS用例编号：F9------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.modifyRecord01IPV6IP,
            recordTTL=self.modifyRecord01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        # 判断是否解析结果既不是self.record01IPV4IP也不是self.recordForDefaultIPV4IP
        self.assertEqual(state, 'true')

    '''
    重定向
    '''
    @unittest.skip("不执行")
    def test_G0_AddRedirectionsRedirectForIPV4(self):
        """
        测试内容：
            对self.view01Name视图新建间接重定向A类型
        测试步骤：
            1.获取viewId
            2.新增重定向，方式为间接重定向，类型为A
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：G0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        res = self.dbo.addRedirectionsCommon(
            domainName=domainName,
            viewName=self.view01Name,
            url=self.urlPath,
            header=self.header,
            recordIP=self.recordForRedirectionsIPV4IP,
            recordTTL=self.recordForRedirectionsTTL,
            analysisType="A",
            redirectType="redirect"
        )
        logging.info("获取新建的重定向：%s" % res)
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_G1_AddRedirectionsRedirectForIPV6(self):
        """
        测试内容：
            对self.view01Name视图新建间接重定向A类型
        测试步骤：
            1.获取viewId
            2.新增重定向，方式为间接重定向，类型为AAAA
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：G1------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        res = self.dbo.addRedirectionsCommon(
            domainName=domainName,
            viewName=self.view01Name,
            url=self.urlPath,
            header=self.header,
            recordIP=self.recordForRedirectionsIPV6IP,
            recordTTL=self.recordForRedirectionsTTL,
            analysisType="AAAA",
            redirectType="redirect"
        )
        logging.info("获取新建的重定向：%s" % res)
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_G2_delZoneForDefault(self):
        """
        测试内容：
            删除default中的zoneSameName
        测试步骤：
            1.获取viewID-获取zoneID-删除zone
        预期结果：1.删除成功，查询是否还存在zoneSameName
        """
        logging.info("------------------mokeForDNS用例编号：G2------------------")
        state = self.dbo.delZoneCommon(viewName="default", zoneName=self.zoneSameName, url=self.urlPath, header=self.header)
        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_G3_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal02Server终端解析view01中的A类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.modifyRecord01IPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：G3------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.modifyRecord01IPV4IP,
            recordTTL=self.modifyRecord01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_G4_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal02Server终端解析view01中的AAAA类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.modifyRecord01IPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：G4------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.modifyRecord01IPV6IP,
            recordTTL=self.modifyRecord01TTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_G5_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal01Server终端解析view01中的A类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：G5------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.recordForRedirectionsIPV4IP,
            recordTTL=self.recordForRedirectionsTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_G6_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal01Server终端解析view01中的AAAA类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：G6------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.recordForRedirectionsIPV6IP,
            recordTTL=self.recordForRedirectionsTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_G7_AddRedirectionsRpzForIPV4(self):
        """
        测试内容：
            对self.view01Name视图新建直接重定向A类型
        测试步骤：
            1.获取viewId
            2.新增重定向，方式为直接重定向，类型为A
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：G7------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        res = self.dbo.addRedirectionsCommon(
            domainName=domainName,
            viewName=self.view01Name,
            url=self.urlPath,
            header=self.header,
            recordIP=self.recordForRedirectionsRpzIPV4IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            analysisType="A",
            redirectType="rpz"
        )
        logging.info("获取新建的重定向：%s" % res)
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_G8_AddRedirectionsRpzForIPV6(self):
        """
        测试内容：
            对self.view01Name视图新建直接重定向AAAA类型
        测试步骤：
            1.获取viewId
            2.新增重定向，方式为直接重定向，类型为AAAA
        预期结果：1.创建成功
        """
        logging.info("------------------mokeForDNS用例编号：G8------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        res = self.dbo.addRedirectionsCommon(
            domainName=domainName,
            viewName=self.view01Name,
            url=self.urlPath,
            header=self.header,
            recordIP=self.recordForRedirectionsRpzIPV6IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            analysisType="AAAA",
            redirectType="rpz"
        )
        logging.info("获取新建的重定向：%s" % res)
        self.assertEqual(res['name'], self.zoneSameName)

    @unittest.skip("不执行")
    def test_G9_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal02Server终端解析view01中的A类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsRpzIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：G9------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.recordForRedirectionsRpzIPV4IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_H0_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal02Server终端解析view01中的AAAA类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal02Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsRpzIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：H0------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.recordForRedirectionsRpzIPV6IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_H1_analysisRecordForIPV4(self):
        """
        测试内容：
            terminal01Server终端解析view01中的A类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s a @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsRpzIPV4IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：H1------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="A",
            recordIP=self.recordForRedirectionsRpzIPV4IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')

    @unittest.skip("不执行")
    def test_H2_analysisRecordForIPV6(self):
        """
        测试内容：
            terminal01Server终端解析view01中的AAAA类型域名,视图中acl为acl02:self.acl02Ip(192.168.0.0)
        测试步骤：
            1.在terminal01Server终端中输入命令  dig %s aaaa @dnsServer02 %(self.recordSameName + "." + self.zoneSameName)
        预期结果：返回ip为self.recordForRedirectionsRpzIPV6IP，TTL值为200
        """
        logging.info("------------------mokeForDNS用例编号：H2------------------")
        domainName = self.recordSameName + "." + self.zoneSameName
        state = self.dbo.analysisRecordCommon(
            terminaServer=self.urlPathYaml["terminal02Server"],
            terminaUsername=self.urlPathYaml["terminal02Username"],
            terminaPassword=self.urlPathYaml["terminal02Password"],
            analysisType="AAAA",
            recordIP=self.recordForRedirectionsRpzIPV6IP,
            recordTTL=self.recordForRedirectionsRpzTTL,
            domainName=domainName,
            DNSServer=self.urlPathYaml["dnsServer01"]
        )

        self.assertEqual(state, 'true')




