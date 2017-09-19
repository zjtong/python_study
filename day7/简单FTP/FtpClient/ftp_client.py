import socket
import os ,json
import optparse #处理命令行参数
import getpass
import hashlib
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
print(BASE_DIR )
import settings
from settings import STATUS_CODE


class FTPClient(object):
    def __init__(self):
        self.make_connection()

    def make_connection(self):
        print("创建连接".center(50, "-"))
        # server = input("server:").strip()
        # port = int(input("port:").strip())
        server = "localhost"
        port = 9999
        # print(type(server),type(port))
        self.sock = socket.socket()
        self.sock.connect((server,port))



    def authenticate(self):
        print("用户认证".center(50, "-"))
        # username = input("username:").strip()
        # password = input("password:").strip()
        username = "admin"
        password = "admin"
        return self.get_auth_result(username,password)

    def get_auth_result(self,username,password):
        data = {'action':'auth',
                'username':username,
                'password':password}

        self.sock.send(json.dumps(data).encode())
        response = self.get_response()
        if response.get('status_code') == 254:
            print("用户 \033[32;1m%s\033[0m 通过认证!"%data["username"])
            self.username = username
            return True
        else:
            print(response.get("status_msg"))

    def get_response(self):
        '''得到服务器端回复结果'''
        data = self.sock.recv(1024)
        # print("server res", data)
        data = json.loads(data.decode())
        print("server res", data)
        return data


    def show_progress(self,total):  #文件传输进度条
        received_size = 0
        current_percent = 0
        while received_size < total:    #收到文件的大小、 文件的总大小
             if int((received_size / total) * 100 )   > current_percent :
                  print("#",end="",flush=True)  #end=""  >>>  不换行
                  current_percent = int((received_size / total) * 100 )
             new_size = yield
             received_size += new_size
 
    def _get(self,cmd_list):
        '''从服务器上下载文件'''
        print("get--",cmd_list)
        if len(cmd_list) == 1:
            print("no filename follows...")
            return
        data_header = {
            'action':'get',
            'filename':cmd_list[1]
         }

        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        print(response)
        if response["status_code"] ==257:#ready to receive
            self.sock.send(b'1')#send confirmation to server 
            base_filename = cmd_list[1].split('\\')[-1]
            received_size = 0
            file_obj = open("%s\%s" % (settings.FILE_SAVE_DIR,base_filename),"wb")

            progress = self.show_progress(response['file_size']) #generator
            progress.__next__()

            while received_size < response['file_size']:
                data = self.sock.recv(4096)
                received_size += len(data)
                file_obj.write(data)
                try:
                  progress.send(len(data))
                except StopIteration as e:
                  print("100%")

            else:
                print("----->file rece done----")
                file_obj.close()


    def _put(self,cmd_list):
        '''上传文件'''
        print("put--",cmd_list)
        if len(cmd_list) == 1:
            print("no filename follows...")
            return
        data_header = {
            'action':'put',
            'filename':cmd_list[1]
         }

        if os.path.isfile(data_header["filename"]):
            file_obj = open(data_header["filename"], "rb")
            file_size = os.path.getsize(data_header["filename"])
            data_header['file_size'] =  file_size
            send_size = 0
        else:
            print("文件路径无效！文件不存在！")
            return
        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        print(response)

        if response["status_code"] ==265:#ready to receive
            self.sock.send(b'1')  # send confirmation to server

            progress = self.show_progress(file_size) #generator
            progress.__next__()
            for line in file_obj :
                self.sock.send(line)
                try:
                  progress.send(len(line))
                except StopIteration as e:
                  print("100%")
            print("文件发送成功！")
            # self.sock.send(b'100')
            file_obj.close()

    def _ls(self,cmd_list):
        '''返回当前目录下的文件列表'''
        print("ls--", cmd_list)
        data_header = {
            'action': 'ls'
        }
        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        #print(response)
        if response["status_code"] == 260:
            print(response["now_dir_path"])
            path_list = response["now_dir_path"].split("\\")
            #print(path_list )
            num = path_list.index("home")
            dir_path = "\\".join(path_list[num+1:])
            #print(dir_path )
            print("\t%s"%dir_path)
            for item in response["dir"]:
                print("\t|----",item)
            for item in response["file"]:
                print("\t|----",item)
        elif response["status_code"] == 261:
            print(STATUS_CODE[261])

    def _cd(self, cmd_list):
        '''切换目录'''
        print("cd--", cmd_list)
        if len(cmd_list) == 1:
            cmd_list.insert(1,"")
        data_header = {
            'action': 'cd',
            "cd_dir": cmd_list[1]
        }

        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        print(STATUS_CODE[response["status_code"]])
        # if response["status_code"] == 263:
        path_list = response["now_dir_path"].split("\\")
        #print(path_list)
        num = path_list.index("home")
        dir_path = "\\".join(path_list[num + 1:])
        #print(dir_path)
        print("服务器当前目录为：",dir_path )

    def _help(self,cmd_list):
        str = '\033[1;36;1m简单FTP指令帮助\033[0m'.center(60, '*') + '\n'
        str = '%shelp -显示帮助\n' % str
        str = '%sls  -显示服务器的当前目录下文件列表\n' % str
        str = '%scd [dir] -切换服务器的目录,dir=要切换到的目录\n' % str
        str = '%s\te.g: cd \:切换到服务器的根目录（个人主页目录）\n' % str
        str = '%s\te.g: cd ..:切换到上一级目录\n' % str
        str = '%s\te.g: cd :切换到当前目录\n' % str
        str = '%sput [filename]  -上传文件到服务器当前目录，filename=完整的本地路\n' % str
        str = '%sget [filename]  -下载服务器上的文件，filename=文件名\n' % str
        print(str)

    def interactive(self):
        retry_count = 0
        while retry_count < 3:
            if self.authenticate():
                print("开始交互".center(50,"-"))
                while True:

                    choice = input("\n请输入指令(输入help显示帮助）[%s]: "%self.username).strip().lower()
                    if len(choice) == 0:continue
                    cmd_list = choice.split()
                    if hasattr(self,"_%s"%cmd_list[0]):
                        func = getattr(self,"_%s"%cmd_list[0])
                        func(cmd_list)
                    else:
                        print("无效的命令！")
            else:
                retry_count +=1
                print('\033[31;1m请重新输入，您还有 %d 次机会！\033[0m\n' % (3 - retry_count ))
        else:
            print("\033[31;1m登录认证失败！即将退出...\033[0m\n")

if __name__ == "__main__":
    ftp = FTPClient()
    ftp.interactive() #交互
