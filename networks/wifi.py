from init import PATH
import time
import configparser
import socket

#网卡类
class Networks:
    """
    初始化配置socket参数
    """
    def __init__(self):
        #读取配置文件
        self.conf = configparser.ConfigParser()
        self.conf.read(PATH()+'init.conf')
        #连接本机
        self.HOST=self.conf.get('networks','url')
        #设置侦听端口
        self.PORT=self.conf.getint('networks','port')
        #设置字节长度
        self.BUFSIZ=1024
        #设置地址
        self.ADDR=(self.HOST,self.PORT)
    """
    与目标服务器建立连接
    返回值：
    Boolean 初始化成功/失败 True/False
    """
    def socketInit(self):
        try:
            print('start connect server')
             #设置客户端
            self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #设置超时时间
            self.client.settimeout(self.conf.getint('networks','timeout'))
            self.client.connect(self.ADDR)
            print('connect server pass')
            return (True)
        except Exception as e:
            print('connect server error:'+str(e))
            return (False)
    """
    向服务器发送请求
    参数:
    String data 数据
    返回值：
    Boolean 发送成功/失败 True/False
    """
    def socketSend(self,data):
        try:
            print("start send");
            #创建发送socket请求
            self.client.send(data.encode('utf8'))
            print('send socket pass:'+data)
            return (True)
        except Exception as e:
            print('send socket error:'+str(e))
            return (False)
    """
    参数:
    空
    返回值：
    String  接受成功 接收到的消息
    Boolean 接受失败 False
    """
    def socketGet(self):
        try:
            print("start get");
            #创建接收socket请求
            data=self.client.recv(self.BUFSIZ).decode('utf8')
            print("get socket pass:"+data);
            return (data)
        except Exception as e:
            print('get socket error:'+str(e))
            return(False)
    """
    参数：
    空
    返回值：
    空
    """
    def socketClose(self):
        try:
            print("start close")
            self.client.shutdown(2)
            self.client.close
            print("close socket pass");
        except Exception as e:
            print('close socket error:'+str(e))