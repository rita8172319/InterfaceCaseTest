import logging
import time
import yaml
import math
import itertools
from itertools import product
from InterfaceModule.Common.getSSH import sshObj
from InterfaceModule.Common.common_fun import Common


class DchpBusinessObj(object):
    def __init__(self):
        # 公共方法
        self.CommonObj = Common()
        # 获取js文件
        jsFileName = 'BaseConversion.js'
        self.jsPath = self.CommonObj.get_JSpath(jsFileName)

    '''
    ipv6到二进制的互转相关业务
    '''

    # ip显示格式化
    def ipFormat(self, num, formatLen, formatType=";"):
        # 二进制隔N位进行显示
        iplist = list(num)
        ip = ''
        index = 1
        for i in iplist:
            ip += i
            if int(index % formatLen) == 0:
                ip += formatType
            index += 1
        return ip

    # 按子网掩码长度获取ipv6前缀
    def ipv6ForPrefix(self, ipv6Addr):
        ipv6List = ipv6Addr.split("/")
        # 补全ipv6
        ipv6 = self.CommonObj.get_des_psswd(jsPath=self.jsPath, funcName="ipv6_to_hex", parameter=ipv6List[0])
        # ipv6转二进制
        ipv6ForTwo = self.CommonObj.get_des_psswd(jsPath=self.jsPath, funcName="hex_to_bin", parameter=ipv6)
        # 根据ipv6截取有效地址
        prefix = ipv6ForTwo[0:int(ipv6List[1])]
        return prefix

    # 根据标识生成每网段全二进制ip
    def IdentificationList(self, Identification):
        # 根据标识划分规则拆分全部二进制组合
        list = []
        for i in range(len(Identification)):
            IdentificationList = []
            for i in product(range(2), repeat=int(Identification[i])):
                tempNum = ''
                for temp01 in i:
                    tempNum += str(temp01)
                IdentificationList.append(tempNum)
            # 根据标识划分规则获得全部二进制组合
            list.append(IdentificationList)
        return list

    # 生成笛卡儿积的ip二进制集合
    def combinationIP(self, identificationList, prefix, completionNum):
        print("ip前缀二进制：", prefix)
        print("ip全标识二进制集合:", identificationList)
        ipAlltempList = []
        if len(identificationList) == 2:
            for x in itertools.product(identificationList[0], identificationList[1]):
                ip = prefix + x[0] + x[1]
                # print(x[0])
                # print(x[1])
                # 二进制补全completionNum位
                ipAll = self.completionIP(ip, completionNum)
                ipAlltempList.append(ipAll)
                # print("ip的笛卡尔乘积：", ipAll)
        elif len(identificationList) == 3:
            for x in itertools.product(identificationList[0], identificationList[1], identificationList[2]):
                ip = prefix + x[0] + x[1] + x[2]
                ipAll = self.completionIP(ip, completionNum)
                ipAlltempList.append(ipAll)
                # print("ip的笛卡尔乘积：", ipAll)
        return ipAlltempList

    # 二进制补全128位
    def completionIP(self, ip, completionNum):
        for i in range(completionNum):
            if len(ip) < completionNum:
                ip += "0"
        return ip

    '''
    ipv4
    '''

    # 按子网掩码长度获取ipv4前缀
    def ipv4ForPrefix(self, ipv6Addr):
        ipv4ListForMask = ipv6Addr.split("/")
        # 补全ipv4
        ipv4List = ipv4ListForMask[0].split(".")
        # print("ipv4:",ipv4List)
        ipv4ForTwoList = []
        for i in ipv4List:
            temp = self.CommonObj.get_des_psswd(jsPath=self.jsPath, funcName="ipv4_to_bin", parameter=i)
            ipv4ForTwoList.append(temp)
        # print("ipv4ForTwoList:",ipv4ForTwoList)
        # ipv4去列表，转为字符串
        ipv4 = ''
        for i in ipv4ForTwoList:
            ipv4 += i
        # ipv4补全32位
        for i in range(32):
            if len(ipv4) < 32:
                ipv4 += "0"
        # print(ipv4)
        # print(len(ipv4))
        return ipv4[0:int(ipv4ListForMask[1])]

    # 二进制转ipv4
    def twoForipv4(self, ipv4AlltempList):
        # ipv4二进制格式化显示
        ipv4FormatList = []
        for i in ipv4AlltempList:
            ipv4Format = self.ipFormat(num=i, formatLen=8, formatType=".")
            ipv4FormatList.append(ipv4Format)
        # 格式化显示
        ipv4TwoList = []
        for i in ipv4FormatList:
            temp = i.split(".")
            tempList = []
            for i in temp:
                if i:
                    tempList.append(i)
            # print(tempList)
            ipv4TwoList.append(tempList)
        # ipv4二进制转ipv4十进制
        ipv4List = []
        for i in ipv4TwoList:
            # print("-----------")
            # print(i)
            ipv4 = ''
            for ipv4One in i:
                temp = str(self.CommonObj.get_des_psswd(jsPath=self.jsPath, funcName="two_to_ipv4", parameter=ipv4One))
                for n in range(3):
                    if len(temp) < 3:
                        temp = "0" + temp
                ipv4 += str(temp)
            ipv4List.append(ipv4)
        return ipv4List


    def runForIpv6(self):
        # 按子网掩码长度分解ipv6
        ipv6ForMask = "2001:DB8::/32"
        Identification = ["3", "2"]
        # 生成网段全二进制ip
        identificationList = self.IdentificationList(Identification)
        # 按子网掩码长度获取ipv6前缀
        prefix = self.ipv6ForPrefix(ipv6ForMask)
        # 组合全二进制ipv6
        ipv6AlltempList = self.combinationIP(identificationList=identificationList, prefix=prefix, completionNum=128)
        # 二进制转ipv6
        for i in ipv6AlltempList:
            ipv6 = self.CommonObj.get_des_psswd(jsPath=self.jsPath, funcName="bin_to_hex", parameter=i)
            ipv6Format = self.ipFormat(num=ipv6, formatLen=4)
            print(ipv6Format)

    def runForIpv4(self):
        # 按子网掩码长度分解ipv4
        ipv4Mask = "192.168.0.0/16"
        Identification = ["2", "2"]
        # 生成网段全二进制ip
        identificationList = self.IdentificationList(Identification)
        print("生成网段全二进制ip:", identificationList)
        # 按子网掩码长度获取ipv4前缀
        prefix = self.ipv4ForPrefix(ipv4Mask)
        print("按子网掩码长度获取ipv4前缀:", prefix)
        # 组合全二进制ipv4
        ipv4AlltempList = self.combinationIP(identificationList=identificationList, prefix=prefix, completionNum=32)
        print(ipv4AlltempList)
        # ipv4二进制转ipv4十进制
        ipv4List = self.twoForipv4(ipv4AlltempList)
        print("ipv4List:",ipv4List)
        for i in ipv4List:
            print(i)

# 11000000101010000001000000000000

if __name__ == '__main__':
    obj = DchpBusinessObj()
    obj.runForIpv4()
