from InterfaceModule.Common.RequestMethod import send_method
import logging

class DnsInterfaceObj(object):
    def __init__(self):
        self.sendMethod = send_method()

    # acl接口
    def aclsInterface(self, url, method,header,data='',aclId=''):
        url = '%s/apis/linkingthing.com/example/v1/acls' % url
        if method == "post":
            res = self.sendMethod.send_post(url=url, data=data, header=header, response_type="json")
        elif method == "get":
            res = self.sendMethod.send_get(url=url, header=header)
        elif method == "put":
            url = url+"/"+aclId
            res = self.sendMethod.send_put(url=url, data=data, header=header, response_type="json")
        elif method == "del":
            url = url+"/"+aclId
            logging.info(url)
            res = self.sendMethod.send_del(url=url, header=header)
        return res

    # view接口
    def viewsInterface(self, url, method, header, data='',viewId=''):
        url = '%s/apis/linkingthing.com/example/v1/views' % url
        if method == "post":
            res = self.sendMethod.send_post(url=url, data=data, header=header, response_type="json")
        elif method == "get":
            res = self.sendMethod.send_get(url=url, header=header)
        elif method == "del":
            url = url + "/" + viewId
            res = self.sendMethod.send_del(url=url, header=header)
        elif method == "put":
            url = url + "/" + viewId
            res = self.sendMethod.send_put(url=url, data=data, header=header, response_type="json")
        return res

    # 区域接口
    def zonesInterface(self, url, method, header,viewId, data='',zoneId=''):
        url = '%s/apis/linkingthing.com/example/v1/views/%s/zones' % (url,viewId)
        if method == "post":
            res = self.sendMethod.send_post(url=url, data=data, header=header, response_type="json")
        elif method == "get":
            res = self.sendMethod.send_get(url=url, header=header)
        elif method == "del":
            url = url+'/'+ zoneId
            res = self.sendMethod.send_del(url=url, header=header)
        return res

    # 区域资源记录
    def rrsInterface(self, url, method, header,viewId,zoneId, data='',rrsId=''):
        url = '%s/apis/linkingthing.com/example/v1/views/%s/zones/%s/rrs' % (url, viewId, zoneId)
        if method == "post":
            res = self.sendMethod.send_post(url=url, data=data, header=header, response_type="json")
        elif method == "get":
            res = self.sendMethod.send_get(url=url, header=header)
        elif method == "put":
            url = url + "/" + rrsId
            res = self.sendMethod.send_put(url=url, data=data, header=header, response_type="json")
        return res

    # 重定向接口
    def redirectionsInterface(self, url, method, header,viewId,data=''):
        url = '%s/apis/linkingthing.com/example/v1/views/%s/redirections' % (url,viewId)
        if method == "post":
            res = self.sendMethod.send_post(url=url, data=data, header=header, response_type="json")
        # elif method == "get":
        #     res = self.sendMethod.send_get(url=url, header=header)
        # elif method == "del":
        #     res = self.sendMethod.send_del(url=url, header=header)
        # elif method == "put":
        #     res = self.sendMethod.send_put(url=url, data=data, header=header, response_type="json")
        return res







