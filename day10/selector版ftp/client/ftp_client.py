# -*- coding: utf-8 -*-

import sys, os,time
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

import socket
import configparser,pickle

class Ftp_Client(object):
    '''
    selector版FTP客户端
    '''
    def __init__(self):
        #创建客户端socket
        self.Client = socket.socket()
        #获取配置文件
        self.Get_Conf()
        #创建连接
        self.Conn()
        #进入命令循环
        self.Command()

    def Get_Conf(self):
        '''
        获取配置信息
        :return:
        '''
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.IP = conf['CLIENT']['ip']
        self.Port = int(conf['CLIENT']['port'])

    def Conn(self):
        self.Client.connect((self.IP,self.Port))

    def Command(self):
        '命令分发'
        self.help()
        while True:
            self.Get_cloudfile_list()
            cmd = input('请输入命令(帮助输入help）：').strip().lower()
            cmd_list = cmd.split()
            if  hasattr(self, "%s" % cmd_list[0]):
                func = getattr(self, "%s" % cmd_list[0])
                func(cmd_list)
            else:
                print('\033[1;31;1m命令错误！\033[0m')
                self.help()

    def Get_cloudfile_list(self):
        data = {
            'act': 'get'
        }
        self.Client.send(pickle.dumps(data))
        # 接收确认信息
        chk = self.Client.recv(1024)
        if chk.decode() == 'ready':
            self.Client.send(b"ok")
            file_list = pickle.loads(self.Client.recv(1024))
            print("云端文件列表".center(50,"-") )
            if file_list :
                for index, item in enumerate(file_list):
                    print("\t",index,item)
            else:
                print("云端无文件，请先上传文件！\n")

    def put(self,cmd_list):
        data = {
            'act':'upload',
            'localfile':cmd_list[1],
            'cloudfile':cmd_list[2]
        }
        if os.path.isfile(data["localfile"]):
            if os.path.getsize(data["localfile"]) == 0:
                print("本地文件为空文件，取消上传！")
                return
        else:
            print("本地文件不存在，取消上传！")
            return
        self.Client.send(pickle.dumps(data))
        #接收确认信息
        chk = self.Client.recv(1024)#up:1
        if chk.decode() == 'ready':
            print('服务端已准备好，开始发送文件...')
            self.Send_File_Size(data)
        elif chk.decode() == 'exist':
            print("云端已存在同名文件！")
        else:
            print('数据传输错误，程序中止')
            exit()
        # return
    def Send_File_Size(self,dict):
        '''
        发送文件大小
        :param dict: 命令字典
        :return:
        '''
        file_path = dict['localfile']
        file_size = os.path.getsize(file_path)
        print('获取大小：',file_size)
        self.Client.send(pickle.dumps(file_size))  # up：2
        file_obj = open(file_path,'rb')
        self.Send_File_Data(file_obj,file_size)#发送文件数据
    def Send_File_Data(self,file_obj,file_size):
        '''
        发送文件数据
        :param file_obj: 文件句柄
        :param file_obj: 文件大小
        :return:
        '''
        #接收确认信息
        send_size = 0
        chk = self.Client.recv(1024)
        if chk.decode() == 'ok':
            print('发送数据')

            while file_size > send_size:
                # print(send_size,file_size)
                data = file_obj.read(4096)
                self.Client.send(data)
                send_size += len(data)


            print("\t文件大小：%s, 发送大小：%s" % (file_size, send_size))
            file_obj.close()
            print("\t文件传输完成！")
        else:
            print('数据传输错误，程序中止')
            exit()


    def check_filepath(self,data):
        '''
        检查文件是否存在（文件名）
        :param filename:
        :return:
        '''
        dir_list = data["localfile"].split("\\")
        file_dir = "\\".join(dir_list[0:-1])
        #print(dir_list)
        if os.path.isdir(file_dir):
            if os.path.isfile(data["localfile"]):
                print("\t本地存在同名文件，取消下载！")
                return False
            else:
                return True
        else:
            print("\t文件存放路径错误，取消下载！")
            return False
    def get(self,cmd_list):
        data = {
            'act': 'download',
            'localfile': cmd_list[2],
            'cloudfile': cmd_list[1]
        }
        if self.check_filepath(data):
            self.Client.send(pickle.dumps(data))
            #接收确认信息
            chk = self.Client.recv(1024)#down:1
            if chk.decode() == 'ready':
                self.Client.send(b'ok')#发送一个消息以激活服务端监听回调 down:2
                self.Get_File_Size(data)
            else:
                print('数据传输错误，程序中止')
                exit()
    def Get_File_Size(self,dict):
        '''
        接收服务端文件大小
        :param dict: 命令字典
        :return:
        '''
        filesize = pickle.loads(self.Client.recv(1024))
        if filesize['size'] == 0:
            print('云端文件不存在！')
        else:
            f = open(dict['localfile'],'wb')
            self.Save_File_Data(f,filesize['size'])
    def Save_File_Data(self,file_obj,file_size):
        '''
        接收服务端发送的文件数据
        :param file_obj: 文件句柄
        :param file_size: 要接收的文件大小
        :return:
        '''
        recved_size = 0
        self.Client.send(b'ok')#发送激活信号 down:3
        while recved_size < file_size :
            if file_size - recved_size > 4096:
                size = 4096
            else:
                size = file_size - recved_size
            # print(recved_size, file_size)
            file_data = self.Client.recv(size)
            recved_size += len(file_data)
            file_obj.write(file_data)
            # file_obj.flush()

        print("文件大小：%s，接收大小：%s" % (file_size, recved_size))
        print('文件下载完成！')
        file_obj.close()

    def help(self,cmd="help"):
        '''
        打印帮助信息
        :return:
        '''
        print('指令格式'.center(50,'-'))
        print('上传文件：put [本地完整路径文件名] [云端文件名]')
        print('下载文件：get [云端文件名] [本地完整路径文件名]\n')

if __name__ == "__main__":
    client = Ftp_Client()