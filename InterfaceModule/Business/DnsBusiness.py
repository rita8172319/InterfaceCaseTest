import logging
import time
from InterfaceModule.Common.getSSH import sshObj
from InterfaceModule.Interface.DnsInterface.DnsInterface import DnsInterfaceObj

class DnsBusinessObj(object):
    def __init__(self):
        # DNS接口类
        self.obj = DnsInterfaceObj()
        
    # 新增记录
    def AddRecordCommon(self, viewName, zoneName, recordName, recordIP, recordTTL, recordType,header,url):
        # 获取视图id
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info(i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)
        # 获取区域id
        res = self.obj.zonesInterface(url=url, method="get", viewId=viewId, header=header)
        zoneId = ''
        for i in res['data']:
            logging.info("获取区域名称：%s" % i['name'])
            if i['name'] == zoneName:
                zoneId = i['id']
        # 新建资源
        data = {"name": recordName, "type": recordType, "value": recordIP, "ttl": recordTTL}
        res = self.obj.rrsInterface(url=url, method="post", viewId=viewId, data=data,
                                    zoneId=zoneId, header=header)
        time.sleep(1)  # 等待生效时间
        return res

    # 修改记录
    def modifyRecordCommon(self, viewName, zoneName, recordName, originalRecordIP, modifyRecordIP, modifyRecordTTL,
                           modifyRecordType, modifyRecordName,header,url):
        # 获取视图id
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info("获得视图信息：%s" % i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)
        # 获取区域id
        res = self.obj.zonesInterface(url=url, method="get", viewId=viewId, header=header)
        zoneId = ''
        for i in res['data']:
            logging.info("获取区域名称：%s" % i['name'])
            if i['name'] == zoneName:
                zoneId = i['id']
        # 获取记录信息
        res = self.obj.rrsInterface(url=url, method="get", viewId=viewId, zoneId=zoneId,
                                    header=header)
        # 修改资源
        data = {
            "id": "",
            "links": {},
            "creationTimestamp": "",
            "deletionTimestamp": "",
            "name": "",
            "type": "",
            "ttl": 200,
            "value": ""
        }
        rrsID = ''
        for i in res["data"]:
            if i['name'] == recordName and i['value'] == originalRecordIP:
                logging.info("获得修改目标信息：%s" % i)
                data['id'] = i['id']
                data['creationTimestamp'] = i['creationTimestamp']
                data['deletionTimestamp'] = i['deletionTimestamp']
                data['name'] = modifyRecordName
                data['type'] = modifyRecordType
                data['ttl'] = modifyRecordTTL
                data['value'] = modifyRecordIP
                data['links'] = i['links']
                rrsID = data['id']

        logging.info("获得修改记录data：%s" % data)
        res = self.obj.rrsInterface(url=url, method="put", viewId=viewId, zoneId=zoneId,
                                    data=data,header=header,rrsId=rrsID)
        time.sleep(1)  # 等待生效时间
        return res

    # 解析域名
    def analysisRecordCommon(self, terminaServer, terminaUsername, terminaPassword, analysisType, domainName, DNSServer,
                             recordIP, recordTTL, isGetResList='false'):
        time.sleep(10)  # 等待生效时间
        # 获取终端连接
        obj = sshObj()
        client = obj.getSSH(
            sys_ip=str(terminaServer),
            username=str(terminaUsername),
            password=str(terminaPassword)
        )
        # 发送命令
        stdin, stdout, stderr = client.exec_command(
            'dig %s %s @%s' % (domainName, analysisType, DNSServer))
        logging.info('dig %s %s @%s' % (domainName, analysisType, DNSServer))
        list = stdout.readlines()
        logging.info(list)
        # 判断结果
        state = 'false'
        for i in list:
            if recordIP.lower() in i:
                i = i.split("\t")
                logging.info(i)
                if '%s.' % (domainName) in i and str(recordTTL) in i:
                    state = 'true'
        client.close()
        if isGetResList == 'false':
            return state
        elif isGetResList == 'true':
            return state, list

    # 新增视图
    def addViewCommon(self, aclName, viewName,header,url):
        # 获取aclip
        res = self.obj.aclsInterface(url=url, method="get", header=header)
        aclid = ''
        for i in res['data']:
            if i['name'] == aclName:
                # logging.info(i)
                logging.info("获取acl：%s，所属id：%s" % (aclName, i["id"]))
                aclid = i["id"]
        # 创建view
        data = {"name": viewName, "aclids": [aclid], "priority": 1}
        res = self.obj.viewsInterface(url=url, method="post", data=data, header=header)
        time.sleep(1)  # 等待生效时间
        return res

    # 删除视图
    def delViewCommon(self,viewName,header,url):
        # 获取视图信息
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        # 判断是否存在self.view01Name的视图，优先级是否为1
        viewID = ""
        for i in res["data"]:
            if i['name'] == viewName:
                viewID = i['id']
        # 删除视图
        res = self.obj.viewsInterface(url=url, method="del", header=header, viewId=viewID)
        time.sleep(1)  # 等待生效时间
        return res

    # 修改视图
    def modifyViewCommon(self, viewName, aclName,header,url):
        # 获取viewID
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewID = ""
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info(i)
                viewID = i['id']
        # 获取aclID
        res = self.obj.aclsInterface(url=url, method="get", header=header)
        aclID = []
        for i in res["data"]:
            if i['name'] == aclName:
                logging.info(i)
                aclID.append(i['id'])
        # 修改view
        data = {"name": viewName, "aclids": aclID, "priority": 1}
        res = self.obj.viewsInterface(url=url, method="put", header=header, data=data,
                                      viewId=viewID)
        # 判断是否修改成功
        # 返回结果中view名称和acl名称是否与修改结果相符
        stateForViewName = False
        stateForAclID = False
        state = 'false'
        if res['name'] == viewName:
            stateForViewName = True
        if res['aclids'][0] == aclID:
            stateForAclID = True
        if stateForViewName + stateForAclID == True:
            state = 'true'
        time.sleep(1)   # 等待生效时间
        return state

    # 新增zone
    def addZoneCommon(self, viewName, zoneName,header,url):
        # 获取视图id
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info(i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)
        # 新建区域
        data = {"name": zoneName, "zonetype": "master"}
        res = self.obj.zonesInterface(url=url, method="post", data=data, viewId=viewId,
                                      header=header)
        time.sleep(1)  # 等待生效时间
        return res

    # 删除zone
    def delZoneCommon(self, viewName, zoneName,header,url):
        # 获取视图id
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info(i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)
        # 获取区域ID
        res = self.obj.zonesInterface(url=url, method="get", viewId=viewId, header=header)
        zoneID = ''
        for i in res["data"]:
            if i['name'] == zoneName:
                logging.info(i)
                zoneID = i['id']
        # 删除区域
        res = self.obj.zonesInterface(url=url, method="del", viewId=viewId, zoneId=zoneID,
                                      header=header)

        # 查询是否删除成功，是否还存在对应区域
        res = self.obj.zonesInterface(url=url, method="get", viewId=viewId, header=header)
        state = 'true'
        for i in res["data"]:
            if i['name'] == zoneName:
                state = 'false'
        time.sleep(1)  # 等待生效时间
        return state

    # 修改acl
    def modifyAclCommon(self, aclName, modifyAclIp,header,url,modifyAclName=''):
        # 获取ACLID,创建时间
        res = self.obj.aclsInterface(url=url, method="get", header=header)
        aclId = ''
        creatTime = ''
        for i in res["data"]:
            if i['name'] == aclName:
                # logging.info(i)
                aclId = i['id']
                creatTime = i['creationTimestamp']
        logging.info("获取aclID：%s" % aclId)
        logging.info("获取creatTime：%s" % creatTime)

        # 修改aclIP or aclName
        if modifyAclName != '':
            aclName = modifyAclName

        data = {"name": aclName, "list": [{"check": "false", "name": modifyAclIp, "type": "ip"}]}
        self.obj.aclsInterface(url=url, method="put", header=header, data=data,
                               aclId=aclId)

        # 获取acl修改后结果
        res = self.obj.aclsInterface(url=url, method="get", header=header)
        modifyCreatTime = ''
        modifyIP = ''
        for i in res["data"]:
            if i['name'] == aclName:
                modifyIP = i['list'][0]['name']
                modifyCreatTime = i['creationTimestamp']
        logging.info("获取creatTime：%s" % modifyCreatTime)
        logging.info("modifyIP：%s" % modifyIP)
        # 查看修改结果
        state = "false"
        if modifyAclIp == modifyIP and creatTime == modifyCreatTime:
            state = "true"
        time.sleep(1)  # 等待生效时间
        return state

    # 删除acl
    def delAclCommon(self, aclName,header,url):
        res = self.obj.aclsInterface(url=url, method="get", header=header)
        # 判断名称是否包含aclName，获取其ID
        aclID = ''
        for i in res['data']:
            if i['name'] == aclName:
                logging.info(i)
                aclID = i["id"]
        # 删除Acl
        res = self.obj.aclsInterface(url=url, method="del", header=header, aclId=aclID)
        time.sleep(1)  # 等待生效时间
        return res

    # 新增重定向
    def addRedirectionsCommon(self, viewName, domainName,url,header,recordIP,recordTTL,redirectType,analysisType):
        # 获取视图id
        res = self.obj.viewsInterface(url=url, method="get", header=header)
        viewId = ''
        for i in res["data"]:
            if i['name'] == viewName:
                logging.info(i)
                viewId = i['id']
        logging.info("获取viewID：%s" % viewId)

        # 新建重定向
        data = {"name":domainName,"type":analysisType,"value":recordIP,"ttl":recordTTL,"redirecttype":redirectType}
        res = self.obj.redirectionsInterface(url=url, method="post", data=data, viewId=viewId,
                                      header=header)
        time.sleep(1)  # 等待生效时间
        return res