import socket
import os ,sys,json
import hashlib
import logging
from logging import handlers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
import settings
from settings import STATUS_CODE


class FTPClient(object):
    def __init__(self):
        self.make_connection()



    def make_connection(self):
        print(" 创建连接 ".center(76, "-"))
        # server = input("server:").strip()
        # port = int(input("port:").strip())
        server = "localhost"
        port = 9999
        # print(type(server),type(port))
        self.sock = socket.socket()
        self.sock.connect((server,port))

    def creat_logger(self,username):
        logger = logging.getLogger(__name__)

        log_file = "%s\\%s\\client.log"%(settings.LOG_DIR,username)
        fh = handlers.RotatingFileHandler(filename=log_file,maxBytes=10485760,backupCount=3)
        # fh = handlers.TimedRotatingFileHandler(filename=log_file, when="S", interval=5, backupCount=3)

        formatter = logging.Formatter('%(asctime)s--%(message)s')

        fh.setFormatter(formatter)
        #fh.setLevel(logging.WARNING )
        logger.addHandler(fh)
        self.logger = logger


    def authenticate(self):
        print(" 用户认证 ".center(76, "-"))
        username = input("username:").strip()
        password = input("password:").strip()
        # username = "admin"
        # password = "admin"
        return self.get_auth_result(username,password)

    def get_auth_result(self,username,password):
        m = hashlib.md5()
        print(password.encode())
        m.update(password.encode())
        password = m.hexdigest()
        print(password)
        data = {'action':'auth',
                'username':username,
                'password':password}
        print(data)
        self.sock.send(json.dumps(data).encode())
        response = self.get_response()
        if response.get('status_code') == 254:
            print("用户 \033[32;1m%s\033[0m 通过认证!"%data["username"])
            self.creat_logger(username)
            self.username = username
            self.server_now_path = "%s"%username
            # self.logger.warning("%s-通过认证-finish" % (username))
            return True
        else:
            print(response.get("status_msg"))
            # self.logger.warning("%s-认证失败-finish" % (username))

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
 
    def _get(self,cmd_list,size = 0):
        '''从服务器上下载文件'''
        print("get--",cmd_list)
        if len(cmd_list) == 1:
            print("no filename follows...")
            return
        data_header = {
            'action':'get',
            'filename':cmd_list[1],
            "received_size": size
         }


        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        self.status = response["status_msg"]
        print(response)
        if response["status_code"] ==267:
            print(settings.STATUS_CODE[267])
        elif response["status_code"] ==257:#ready to receive
            base_filename = cmd_list[1].split('\\')[-1]

            received_size = 0
            file_path = "%s\%s" % (settings.FILE_SAVE_DIR,base_filename)

            if os.path.isfile(file_path) :
                if response['file_size'] == os.path.getsize(file_path):
                    print("文件已存在！")
                    self.status = "文件已存在！"
                    self.sock.send(b'2')  # send confirmation to server
                    return
            self.sock.send(b'1')  # send confirmation to server
            file_obj = open(file_path ,"ab")
            md5_obj = hashlib.md5()
            progress = self.show_progress(response['file_size']) #generator
            progress.__next__()
            while received_size < response['file_size']:
                data = self.sock.recv(4096)
                received_size += len(data)
                try:
                  progress.send(len(data))
                except StopIteration as e:
                  print("100%")
                file_obj.write(data)
                md5_obj.update(data)
            else:
                print("----->file rece done----")
                file_obj.close()
                md5_val = md5_obj.hexdigest()
                md5_from_server = self.get_response()
                if md5_from_server['status_code'] == 258:
                    if md5_from_server['md5'] == md5_val:
                        print("%s 文件一致性校验成功!" % base_filename)
                        self.status = "文件获取成功，一致性校验成功!"
                    else:
                        self.status = "文件获取成功，一致性校验失败!"

                #print(md5_val,md5_from_server)

    def _put(self,cmd_list,dir=""):
        '''上传文件'''
        print("put--",cmd_list)
        if len(cmd_list) == 1:
            print("no filename follows...")
            return
        data_header = {
            'action':'put',
            'filename':cmd_list[1],
            "dir" : dir
         }


        if os.path.isfile(data_header["filename"]):
            file_obj = open(data_header["filename"], "rb")
            file_size = os.path.getsize(data_header["filename"])
            data_header['file_size'] =  file_size
            #send_size = 0
        else:
            print("文件路径无效！文件不存在！")
            self.status = "文件路径无效！文件不存在！"
            return
        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        print(response)
        self.status = response["status_msg"]
        if response["status_code"] ==265:#ready to receive
            self.sock.send(b'1')  # send confirmation to server

            md5_obj = hashlib.md5()
            progress = self.show_progress(file_size-response["size"]) #generator
            progress.__next__()
            file_obj.seek(response["size"])
            for line in file_obj:
                self.sock.send(line)
                try:
                  progress.send(len(line))
                except StopIteration as e:
                  print("100%")
                md5_obj.update(line)
            else:
                print("文件发送成功！")
                file_obj.close()
                md5_val = md5_obj.hexdigest()
                md5_from_server = self.get_response()
                if md5_from_server['status_code'] == 258:
                    if md5_from_server['md5'] == md5_val:
                        print("%s 文件一致性校验成功!" % data_header["filename"])
                        self.status = "文件发送成功！一致性校验成功!"
                    else:
                        self.status = "文件发送成功！一致性校验失败!"
                #print(md5_val,md5_from_server)
        elif response["status_code"] ==266:
            print(STATUS_CODE[266])



    def _ls(self,cmd_list):
        '''返回当前目录下的文件列表'''
        print("ls--", cmd_list)
        data_header = {
            'action': 'ls'
        }
        self.sock.send(json.dumps(data_header).encode())
        response = self.get_response()
        self.status = response["status_msg"]
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
        self.status = response["status_msg"]
        print(STATUS_CODE[response["status_code"]])
        # if response["status_code"] == 263:
        path_list = response["now_dir_path"].split("\\")
        #print(path_list)
        num = path_list.index("home")
        dir_path = "\\".join(path_list[num + 1:])
        #print(dir_path)
        self.server_now_path  = dir_path
        print("服务器当前目录为：",dir_path )


    def _help(self,cmd_list):
        str = '\033[1;36;1m简单FTP指令帮助\033[0m'.center(60, '*') + '\n'
        str = '%shelp -显示帮助\n' % str
        str = '%sls  -显示服务器的当前目录下文件列表\n' % str
        str = '%scd [dir] -切换服务器的目录,dir=要切换到的目录\n' % str
        str = '%s\te.g: cd \:切换到服务器的根目录（个人主页目录）\n' % str
        str = '%s\te.g: cd ..:切换到上一级目录\n' % str
        str = '%s\te.g: cd :切换到当前目录\n' % str
        str = '%sput [filename]  - 上传文件到服务器当前目录，filename=完整的本地路\n' % str
        str = '%sget [filename]  - 下载服务器上的文件，filename=文件名\n' % str

        print(str)

    def unfinish(self):
        filename = "%s\\%s\\client.log" % (settings.LOG_DIR, self.username)
        lastline = ""
        with open(filename, encoding="gbk") as f:
            for line in f:
                lastline = line

        if self.username in lastline and "finish" in lastline:
            return
        else:
            choice = input("上次退出时有未完成任务，是否继续..."
                           "不继续请按：N\\n>>>").strip().lower()
            if choice != "n":
                last_cmd = lastline.split("--")[-1]
                print(last_cmd)
                cmd_list = eval(last_cmd.split("-")[1])
                dir = last_cmd.split("-")[2]
                print("cmd_list:",cmd_list)
                print("dir:", dir)
                # data = {"cmd_list": cmd_list, "dir": dir}
                # print(data)

                if cmd_list[0] == "get":
                    file_abs_path = "%s\%s"%(settings.FILE_SAVE_DIR,cmd_list[1].split("\\")[-1])
                    file_size = os.path.getsize(file_abs_path)
                    self._get(cmd_list,file_size)
                    self.logger.warning("%s-%s-%s-finish" % (self.username, cmd_list, self.status))
                elif cmd_list[0] == "put":
                    dir_list = dir.split("\\")
                    del dir_list[0]
                    base_dir = "\\".join(dir_list )
                    print("base_dir",base_dir)
                    self._put(cmd_list,base_dir)
                    self.logger.warning("%s-%s-%s-finish" % (self.username, cmd_list, self.status))


    def interactive(self):
        retry_count = 0
        while retry_count < 3:

            if self.authenticate():
                print(" 开始交互 ".center(76,"-"))
                self.unfinish()


                while True:
                    print("".center(80, "-"))
                    choice = input("请输入指令(输入help显示帮助,输入exit退出）[%s]: "%self.username).strip().lower()
                    if choice == "exit":
                        exit()
                    if len(choice) == 0:continue
                    cmd_list = choice.split()
                    if hasattr(self,"_%s"%cmd_list[0]):
                        func = getattr(self,"_%s"%cmd_list[0])
                        self.logger.warning("%s-%s-%s-start"%(self.username ,cmd_list,self.server_now_path ))
                        func(cmd_list)
                        self.logger.warning("%s-%s-%s-finish" % (self.username,cmd_list,self.status))
                    else:
                        print("无效的命令！")
            else:
                retry_count +=1
                print('\033[31;1m请重新输入，您还有 %d 次机会！\033[0m\n' % (3 - retry_count ))
        else:
            print("\033[31;1m登录认证失败！即将退出...\033[0m\n")

if __name__ == "__main__":
    ftp_client = FTPClient()
    ftp_client.interactive() #交互
