import smtplib,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.image import MIMEImage

class email(object):
    def __init__(self):
        #设置登录及服务器信息
        self.mail_host = 'smtp.163.com'           #发送邮箱服务器
        self.mail_user = 'sdasadtest@163.com'    #发送人邮箱账号
        self.mail_pwd = 'r123456'                #发送人密码
        self.sender = 'sdasadtest@163.com'       #发送人邮箱
        self.receivers = '1919349170@qq.com'     #接收人邮箱

        #设置eamil信息
        #添加一个MIMEmultipart类，处理正文及附件
        self.message = MIMEMultipart()
        self.message['From'] = self.sender
        self.message['To'] = self.receivers
        self.message['Subject'] = '邮件测试'      #发送邮件主题
        self.message['Date'] = formatdate( )
        #设定发送文件主体内容
        self.msg = MIMEText('<html>dx测试报告</html>','html','utf-8')
        # 将内容附加到邮件主体中
        self.message.attach(self.msg)

    #获取测试报告最新文件
    def get_filename(self):
        file_dir = '../report'
        for root, dirs, files in os.walk(file_dir):
            # print(root)  # 当前目录路径
            # print(dirs)  # 当前路径下所有子目录
            # print(files)  # 当前路径下所有非目录子文件
            files.sort()
            self.filename=files[-3] #获取发送文件名称，用于编写发送文件名
            files = os.path.join('../report/'+files[-3]) #获取文件发送目录，用于发送文件
            return files

    # 添加照片附件
    def email_image(self):
        fp = open('1.png','rb')
        picture = MIMEImage(fp.read())

        # 附件设置内容类型，方便起见，设置为二进制流
        picture['Content-Type'] = 'application/octet-stream'
        # 设置附件头，添加文件名
        picture['Content-Disposition'] = 'attachment;filename="1.png"'

        fp.close()
        self.message.attach(picture)  # 将内容附加到邮件主体中

    # 添加txt附件
    def email_txt(self):
        fp = open('1.txt','rb')
        txt = MIMEText(fp.read(),'plain','utf-8')
        txt['Content-Type'] = 'application/octet-stream'
        txt['Content-Disposition'] = 'attachment;filename="1.txt"'
        fp.close()
        self.message.attach(txt)    # 将内容附加到邮件主体中

    # 添加html附件
    def email_html(self):
        filename=self.get_filename()#   获取最新html报告
        fp = open(filename,'rb')
        html = MIMEText(fp.read(),'html','utf-8')
        html['Content-Type'] = 'application/octet-stream'
        html['Content-Disposition'] = 'attachment;filename=%s'%(self.filename)
        fp.close()
        self.message.attach(html)  # 将内容附加到邮件主体中

    #发送
    def email_send(self):
        #需要SSL认证
        smtpObj = smtplib.SMTP_SSL(self.mail_host)       #发送邮箱服务器
        smtpObj.login(self.mail_user,self.mail_pwd)          #登录发送邮箱
        smtpObj.sendmail(self.sender,self.receivers,self.message.as_string())
        print('success')
        smtpObj.quit()

if __name__ == '__main__':
    e = email()
    e.email_html()  #发送包含html附件
    e.email_send() #发送文件
    # e.get_filename()
    # e.email_image() #发送包含图片附件
    # e.email_txt()   #发送包含txt附件