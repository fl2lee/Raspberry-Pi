import configparser
import sys
import time
from init import PATH
from networks import networks
from gpio import gpio

def conf(state=0):
    #读取配置文件
    conf = configparser.ConfigParser()
    conf.read(PATH()+'init.conf')
    #获取sn
    sn=conf.get('networks','sn')
    #获取key
    key=conf.get('networks','key')
    if(sn=='' or key==''):
        state=1
    if(state==1):
        sn=input('please input sn:')
        key=input('please input key:')
        conf.set('networks','sn',sn)
        conf.set('networks','key',key)
        conf.write(open(PATH()+'init.conf',"w"))
    return {'sn':sn,'key':key}
def main():
    while 1:
        try:
            config=conf()
            print(config)
            sn=config['sn']
            key=config['key']
            #防止资源占用率过高导致树莓派死机
            time.sleep(0.01)
            #是否注册
            isRegister=0
            #是否初始化IO口
            isIoInit=0
            #初始化网络连接
            if(networks.socketInit()==True):
                #发送注册消息
                if(networks.socketSend('#1@'+sn+'@'+key+'#')==True):
                    while 1:
                        #接收消息
                        data=networks.socketGet()
                        if(data!=False):
                            if data!=None:
                                #切割接收到的信息
                                dataResolve=data.split('#')
                                dataResolve=dataResolve[1].split('@')
                                if(dataResolve[0]=='0'):
                                    print ('心跳')
                                elif(dataResolve[0]=='-1'):
                                    break
                                #判断是否注册过
                                elif(isRegister==0):
                                    if(dataResolve[0]=='1'):
                                        #如果注册失败
                                        if(dataResolve[1]!='1'):
                                            conf(1)
                                            print('Register failure')
                                            break
                                        print('Register success')
                                        isRegister=1
                                        if(networks.socketSend('#2@#')==False):
                                            break
                                #判断是否初始化过
                                elif(isIoInit==0):
                                    if(dataResolve[0]=='2'):
                                        #如果获取IO信息失败
                                        if(dataResolve[1]!='1'):
                                            print('Get I/O info failure')
                                            break
                                        if(dataResolve[2]!=''):
                                            networks.socketSend('#3@'+gpio.ioMamage(dataResolve[2]))
                                        else:
                                            networks.socketSend('#3@'+gpio.getIoInfo())
                                        print('Get I/O info success')
                                        isIoInit=1
                                #如果注册过而且IO初始化过则进入循环接收模式
                                elif(isRegister==1 and isIoInit==1):
                                    #等待IO控制命令
                                    if(dataResolve[0]=='3'):
                                        networks.socketSend('#3@'+gpio.ioMamage(dataResolve[2]))
                                #没有注册则退出
                                else:
                                    break
                                networks.socketSend('#0@#')
                        else:
                            break
                #关闭网络连接
                networks.socketClose()
        except Exception as e:
            networks.socketClose()
            print(str(e))
if __name__ == '__main__':
    main()
