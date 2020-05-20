import paramiko

# 远程登陆操作系统
class sshObj(object):
    def __init__(self):
        pass
    def getSSH(self, sys_ip, username, password):
        # 开启服务器
        try:
            # 创建ssh客户端
            self.client = paramiko.SSHClient()
            # 第一次ssh远程时会提示输入yes或者no
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 密码方式远程连接
            self.client.connect(sys_ip, 22, username=username, password=password, timeout=20)
        except Exception as e:
            print(e)
        finally:
            pass

        return self.client




