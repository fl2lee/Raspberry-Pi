from RPi import GPIO
import json



#Io类
class IoManage:
    """
    初始化配置IoManage类参数
    """
    def __init__(self):
        self.GPIO=GPIO
        self.GPIO.cleanup()
        self.GPIO.setmode(self.GPIO.BCM)
        #bcm编码
        self.bcm_info={
                        "2":["0","0"],"3":["0","0"],"4":["0","0"],"17":["0","0"],"27":["0","0"],"22":["0","0"],"10":["0","0"],"9":["0","0"],"11":["0","0"],"0":["0","0"],"5":["0","0"],"6":["0","0"],"13":["0","0"],"19":["0","0"],"26":["0","0"],
                        "14":["0","0"],"15":["0","0"],"18":["0","0"],"23":["0","0"],"24":["0","0"],"25":["0","0"],"8":["0","0"],"7":["0","0"],"1":["0","0"],"12":["0","0"],"16":["0","0"],"20":["0","0"],"21":["0","0"]
                        }
    """
    初始化GPIO设置（目前仅支持布尔型OUT类型的初始化）
    参数
        String(json) ioConfig io设置信息
            格式：{ "BCM_NUM" : [ io_type , io_state ] , "BCM_NUM" : [ io_type , io_state ] }
                BCM_NUM GPIO的BCM码
                io_type GPIO当前模式 0->未设置/其他 1->OUT 2->IN(未开放) 3->PWM(待开发) 4->SPI(待开发) 5->I2C(待开发) 6->SERIAL(待开发)
                io_state io_type=0->无效 io_type=1->0/1 低电平/高电平 io_type=2->无效 io_type=3->占空比(待开发) io_type=4->(待开发) io_type=5->(待开发) io_type=6->(待开发)
    返回值
        String(json) 当前GPIO状态
            参考def getIoInfo()
    """
    def ioMamage(self,ioConfig):
        ioConfigArr=json.loads(ioConfig)
        for bcm_key in ioConfigArr:
            #bcm码
            bcm_num=int(bcm_key)
            #io类型
            io_type=int(ioConfigArr[bcm_key][0])
            #io状态
            io_state=int(ioConfigArr[bcm_key][1])
            #如果GPIO为OUT类型
            if(io_type==1):
                self.GPIO.setup(bcm_num,self.GPIO.OUT)
                #设置GPIO的电平状况
                if(io_state==0):
                    self.GPIO.output(bcm_num,self.GPIO.LOW)
                elif(io_state==1):
                    self.GPIO.output(bcm_num,self.GPIO.HIGH)
            #如果GPIO为IN类型
            #else if(ioConfigArr[bcm_key][0]==2):
            #    self.GPIO.setup(bcm_num,self.GPIO.IN)
        return self.getIoInfo()
    """
    获取GPIO状态
    参数
    无
    返回值
        String(json) ioConfig io设置信息
            格式：{ "BCM_NUM" : [ io_type , io_state ] , "BCM_NUM" : [ io_type , io_state ] }
                BCM_NUM GPIO的BCM码
                io_type GPIO当前模式 0->未设置 1->OUT 2->IN 3->PWM 4->SPI 5->I2C 6->SERIAL
                io_state io_type=0->无效 io_type=1->0/1 低电平/高电平 io_type=2->0/1 低电平/高电平 io_type=3->占空比(待开发) io_type=4->(待开发) io_type=5->(待开发) io_type=6->(待开发)
    """
    def getIoInfo(self):
        for bcm_key in self.bcm_info:
            #bcm码
            bcm_num=int(bcm_key)
            #判断IO类型
            io_type=self.GPIO.gpio_function(bcm_num)
            if(io_type==self.GPIO.OUT):
                self.bcm_info[bcm_key][0]="1"
                #防止GPIO被其他脚本占用导致无法成功检测
                self.GPIO.setup(bcm_num,self.GPIO.OUT)
                #防止以后库函数更新导致LOW和HIGH对应数值发生变化所以使用IF而非直接赋值
                if(self.GPIO.input(bcm_num)==self.GPIO.LOW):
                    self.bcm_info[bcm_key][1]="0"
                else:
                    self.bcm_info[bcm_key][1]="1"
            elif(io_type==self.GPIO.IN):
                self.bcm_info[bcm_key][0]="2"
            elif(io_type==self.GPIO.HARD_PWM):
                self.bcm_info[bcm_key][0]="3"
            elif(io_type==self.GPIO.SPI):
                self.bcm_info[bcm_key][0]="4"
            elif(io_type==self.GPIO.I2C):
                self.bcm_info[bcm_key][0]="5"
            elif(io_type==self.GPIO.SERIAL):
                self.bcm_info[bcm_key][0]="6"
            else:
                self.bcm_info[bcm_key][0]="0"
        return json.dumps(self.bcm_info)
            
            