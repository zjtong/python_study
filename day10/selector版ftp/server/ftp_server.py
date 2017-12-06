# -*- coding: utf-8 -*-

import sys, os,time

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
# print(path)
base_path = "%s\\file" % path


import socket
import selectors
import configparser,pickle


class Ftp_Server(object):
    '''
    selectors版FTP，IO多路复用
    '''
    def __init__(self):
        self.Sel = selectors.DefaultSelector()
        self.Action = {}#存储每个连接的命令，以conn作为标识
        self.File_Obj = {}#存储每个连接的FTP文件信息，以conn作为标识

        #获取配置文件
        self.Get_Conf()
        #创建socket
        self.Handle()

    def Handle(self):
        sock = socket.socket()
        sock.bind((self.IP,self.Port))
        sock.listen()
        sock.setblocking(False)#默认不阻塞
        #注册selector事件
        self.Sel.register(sock,selectors.EVENT_READ,self.Accept)
        while True:
            events = self.Sel.select()
            for key , mask in events:
                #print(key,mask)
                #print('活动IO：',key.fileobj)
                #print('回调：',key.db)
                callback = key.data
                callback(key.fileobj)

    def Get_Conf(self):
        '''
        获取配置信息
        :return:
        '''
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.IP = conf['SERVER']['ip']
        self.Port = int(conf['SERVER']['port'])

    def Accept(self,sock):
        conn,addr = sock.accept()
        self.addr = addr
        print('客户端接入:',addr)
        conn.setblocking(False)#设置不阻塞
        self.Sel.register(conn,selectors.EVENT_READ,self.Read)

    def Read(self,conn):
        '''
        读取客户端过来的命令
        :return:
        '''
        try:

            cmd = conn.recv(1024)
            if cmd:
                #print(pickle.loads(cmd))
                cmd_dict = pickle.loads(cmd)
                if cmd_dict['act'] == 'upload':
                    if self.check_filename(cmd_dict['cloudfile']):
                        conn.send(b'exist') #文件已存在
                        self.Sel.unregister(conn)
                        self.Sel.register(conn, selectors.EVENT_READ, self.Read)
                    else:
                        conn.send(b'ready')  # 发送确认信息防止粘包 up:1
                        self.Action[conn] = cmd_dict#参数存储进字典
                        #重新注册事件，以更换回调函数，进入接收文件大小
                        self.Sel.unregister(conn)
                        self.Sel.register(conn,selectors.EVENT_READ,self.UpLoad_Get_FileSize)
                        print("\t",self.Action[conn])
                elif cmd_dict['act'] == 'download':
                    conn.send(b'ready')# 发送确认信息防止粘包 down:1
                    self.Action[conn] = cmd_dict
                    # 重新注册事件，以更换回调函数，进入发送文件大小
                    self.Sel.unregister(conn)
                    self.Sel.register(conn,selectors.EVENT_READ,self.DownLoad_Send_FileSize)
                elif cmd_dict['act'] == 'get':

                    conn.send(b'ready')  # 发送确认信息防止粘包 down:1
                    self.Action[conn] = cmd_dict
                    # 重新注册事件，以更换回调函数
                    self.Sel.unregister(conn)
                    self.Sel.register(conn, selectors.EVENT_READ, self.Get_file_list)

            else:
                self.Sel.unregister(conn)
                conn.close()
        except Exception as e:
            self.Sel.unregister(conn)
            conn.close()
            print(e)

    def Get_file_list(self,conn):

        file_list = os.listdir(base_path)
        chk = conn.recv(1024)
        if chk.decode() == 'ok'and file_list:
            conn.send(pickle.dumps(file_list ))
        else:
            conn.send(pickle.dumps([]))
        self.Sel.unregister(conn)
        self.Sel.register(conn, selectors.EVENT_READ, self.Read)
        del self.Action[conn]



    def DownLoad_Send_FileSize(self,conn):
        '''
        发送下载文件大小
        :param conn:
        :param mask:
        :return:
        '''
        data = {'size':0}
        print('\t文件下载：',self.Action[conn]['cloudfile'])
        chk = conn.recv(1024)#down:2 接收一个激活信号
        filename = "%s\\%s"%(base_path ,self.Action[conn]['cloudfile'])
        if os.path.isfile(filename):#判断文件是否存在
            data['size'] = os.path.getsize(filename)
            print("\t文件大小：",data['size'])
            conn.send(pickle.dumps(data))#发送文件大小
            f = open(filename,'rb')
            self.File_Obj[conn] = {
                'file_obj': f,
                'filesize': data['size'],
                'sendsize' : 0

            }
            #重新注册监听事件
            self.Sel.unregister(conn)
            self.Sel.register(conn,selectors.EVENT_READ,self.DownLoad_Send_FileDta)
        else:
            conn.send(pickle.dumps(data))  # 发送0大小，标识文件不存在
            print("\t云端文件不存在！")
            #回到read回调监听
            self.Sel.unregister(conn)
            self.Sel.register(conn, selectors.EVENT_READ, self.Read)
            del self.Action[conn]
    def DownLoad_Send_FileDta(self,conn):
        '''
        发送下载文件数据
        :param conn:
        :param mask:
        :return:
        '''
        chk = conn.recv(2)#接收接货信号 down:3
        #print(self.File_Obj[conn])
        file_obj = self.File_Obj[conn]['file_obj']
        file_size = self.File_Obj[conn]['filesize']
        send_size = 0
        count = 1

        while file_size > send_size :
            try:
                #print(file_size,send_size)
                #print("已发送%d%%，%d字节" % (int(send_size / file_size * 100), send_size))
                data = file_obj.read(4096)
                send_size += len(data)
                conn.send(data)
            except Exception as BlockingIOError:
                time.sleep(0.2)
                conn.send(data)
                count +=1
                continue
        print("\tBlockingIOError异常:", count)
        print("\t文件大小：%s, 发送大小：%s"%(file_size,send_size) )
        file_obj.close()
        print("\t发送文件完成")
        #发送完毕，重新进入read监听
        self.Sel.unregister(conn)
        self.Sel.register(conn, selectors.EVENT_READ, self.Read)
        del self.Action[conn]
        del self.File_Obj[conn]

    def check_filename(self,filename):
        '''
        检查文件是否存在（文件名）
        :param filename:
        :return:
        '''
        #print(filename)
        for root, dirs, files in os.walk(base_path):
            #print(files)
            if filename in files:
                return True
            else:
                return False
    def UpLoad_Get_FileSize(self,conn):
        '''
        接收客户端发送过来的文件大小
        :param conn:
        :param mask:
        :return:
        '''
        print('\t上传文件的路径:',self.Action[conn]['localfile'])
        file_size = pickle.loads(conn.recv(1024))
        print('\t上传文件的大小：',file_size)
        file_path = "%s\\%s"%(base_path ,self.Action[conn]['cloudfile'])
        f = open(file_path,'wb')
        # 将文件信息记录入全局字典
        self.File_Obj[conn] = {
            'file_obj':f,
            'filesize':file_size,#文件总大小
        }
        conn.send(b'ok')#发送验证数据给客户端，防止粘包
        #重新注册事件，将下一个活动IO交给接收文件数据函数处理
        self.Sel.unregister(conn)
        self.Sel.register(conn,selectors.EVENT_READ,self.UpLoad_Get_FileData)

    def UpLoad_Get_FileData(self,conn):
        '''
        接收文件数据
        :return:
        '''
        file_obj = self.File_Obj[conn]['file_obj']
        file_size = self.File_Obj[conn]['filesize']
        recved_size = 0
        count = 0
        while recved_size < file_size :
            # print(file_size, recved_size)
            try:
                if file_size - recved_size > 4096:
                    size =4096
                else:
                    size = file_size - recved_size
                file_data = conn.recv(size)
                recved_size += len(file_data)
                file_obj.write(file_data)
            except Exception as BlockingIOError:
                time.sleep(0.2)
                file_data = conn.recv(size)
                recved_size += len(file_data)
                file_obj.write(file_data)
                count+=1
                # print(count)
                continue
        print("\tBlockingIOError异常:",count)
        print("\t文件大小：%s，接收大小：%s" % (file_size, recved_size))
        print('\t文件下载完成！')
        #conn.recv(1024)
        self.File_Obj[conn]['file_obj'].close()  # 关闭文件
        # 解绑事件
        self.Sel.unregister(conn)
        # #重新注册事件监听
        self.Sel.register(conn, selectors.EVENT_READ, self.Read)
        del self.Action[conn]  # 删除临时数据
        del self.File_Obj[conn]  # 删除文件句柄

if __name__ == "__main__":
    print(" 服务器准备就绪 ".center(73, "-"))
    server = Ftp_Server()


