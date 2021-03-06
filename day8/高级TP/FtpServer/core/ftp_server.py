import socketserver
import configparser
from conf import settings
import os
import hashlib

import json
class FTPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        while True:
            print("".center(80,"-") )
            self.data = self.request.recv(1024).strip()
            print(self.client_address[0])
            # print(self.data)
            if not self.data:
                print("client closed...")
                break
            data  = json.loads(self.data.decode())
            print("data: ",data)
            if data.get('action') is not None:  #判断指令的合法性
                #print("---->",hasattr(self,"_auth"))
                if hasattr(self,"_%s"%data.get('action')):  #反射，判断是否有对应的字符串的方法
                    func = getattr(self,"_%s"% data.get('action'))
                    func(data)
                else:
                    print(settings.STATUS_CODE[251])
                    self.send_response(251)
            else:
                print("无效的命令格式！")
                self.send_response(250)

    def send_response(self,status_code,data=None):
        '''向客户端返回数据'''
        response = {'status_code':status_code,'status_msg':settings.STATUS_CODE[status_code]}
        if data:
            response.update( data  )
        self.request.send(json.dumps(response).encode())


    __auth_flag = False
    def _auth(self,*args,**kwargs):
        data = args[0]
        if data.get("username") is None or data.get("password") is None:
            self.send_response(252)

        user =self.authenticate(data.get("username"),data.get("password"))
        if user is None:
            self.send_response(253)
        else:
            #print("passed authentication",user["Username"],user["Password"])

            self.user = user
            self.Quotation = self.user["Quotation"]
            self.quotation = self.get_quotation()
            self.user_home_dir = "%s\%s" %(settings.USER_HOME,self.user["Username"])
            self.now_dir_path  = self.user_home_dir
            self.__auth_flag = True   #用户认证标志位置1
            self.send_response(254)
    def authenticate(self,username,password):
        '''验证用户合法性，合法就返回用户数据'''
        config = configparser.ConfigParser()
        config.read(settings.ACCOUNT_FILE)
        m = hashlib.md5()
        if username in config.sections():
            m.update(config[username]["Password"].encode())
            _password = m.hexdigest()
            #print(password)
            #print(_password)
            if _password == password:
                print("用户 \033[32;1m%s\033[0m 通过验证！"%username)

                config[username]["Username"] = username
                """config[username]"""
                return config[username]


    def get_dir_size(self):
        size = 0
        file_list = []
        for root, dirs, files in os.walk(self.user_home_dir ):

            # print(root,"\t#",dirs,"\t#",files)
            for name in files:
                file_name = os.path.join(root, name)
                #print(file_name)
                size += os.path.getsize(file_name)
        return size
    def get_quotation(self):
        if "TB" in self.Quotation:
            quotation = int(self.Quotation.replace("TB",""))*1024*1024*1024*1024
        elif "GB" in self.Quotation:
            quotation = int(self.Quotation.replace("GB",""))*1024*1024*1024
        elif "MB" in self.Quotation:
            quotation = int(self.Quotation.replace("MB",""))*1024*1024
        else:
            quotation = int(self.Quotation.replace("KB",""))*1024
        return quotation

    def _put(self,*args,**kwargs):
        "client send file to server"
        data = args[0]
        if data.get('filename') is None:
            self.send_response(255)
            return
        file_size = data["file_size"]
        dir_size = self.get_dir_size()
        if file_size + dir_size +100 > self.quotation:
            self.send_response(266)
            return
        filename = data.get('filename').split('\\')[-1]
        filepath = "%s\\%s"%(self.now_dir_path,filename)
        if len(data.get("dir")) > 0 and data.get("dir") not in self.now_dir_path :
            filepath = "%s\\%s\\%s"%(self.now_dir_path,data.get("dir"),filename )
        #print(filepath )
        if os.path.isfile(filepath):
            if file_size == os.path.getsize(filepath):
                self.send_response(268)
                return

        file_obj = open(filepath, "ab")
        print("000",filepath)
        self.send_response(265,{"size":os.path.getsize(filepath)})
        # else:
        #     self.send_response(265)
        received_size = os.path.getsize(filepath)
        self.request.recv(1)  # 等待客户端确认

        md5_obj = hashlib.md5()
        while received_size < file_size :
            data = self.request.recv(4096)
            file_obj.write(data)
            md5_obj.update(data)
            received_size += len(data)
            #print(data['size'], received_size)
        else:
            print("--- [%s] 文件接收成功！---"%filename)
            file_obj.close()
            md5_val = md5_obj.hexdigest()
            self.send_response(258, {'md5': md5_val})

    def _get(self,*args,**kwargs):
        if self.__auth_flag :
            data = args[0]
            if data.get('filename') is None:
                self.send_response(255)
            #user_home_dir = "%s/%s" %(settings.USER_HOME,self.user["Username"])
            file_abs_path = "%s\%s" %(self.now_dir_path,data.get('filename'))
            size = data.get("received_size")
            print("file abs path",file_abs_path)

            if os.path.isfile(file_abs_path):
                file_obj = open(file_abs_path,"rb")
                file_size = os.path.getsize(file_abs_path)
                if file_size == 0:
                    self.send_response(267)
                    return
                self.send_response(257,data={'file_size':file_size-size})
                res = self.request.recv(1) #等待客户端确认
                #print("res:",res)
                if res == b"2":
                    return

                md5_obj = hashlib.md5()
                file_obj.seek(size)
                for line in file_obj:
                    self.request.send(line)
                    md5_obj.update(line)
                else:
                    file_obj.close()
                    md5_val = md5_obj.hexdigest()
                    self.send_response(258,{'md5':md5_val})
                    print("send file done....")

            else:
                self.send_response(256)
        else:
            print("用户没有通过验证，没有权限！")


    def _ls(self,*args,**kwargs):
        '''返回云端文件列表'''
        if self.__auth_flag :
            data = args[0]
            print(data)
            print("当前目录：",self.now_dir_path )
            data["now_dir_path"] = self.now_dir_path
            if os.path.exists(self.now_dir_path):
                file_list = os.listdir(self.now_dir_path)
                if file_list:
                    data.update({"file" : []})
                    data.update({"dir" : []})
                    print("目录下的文件列表：",file_list )
                    for item in file_list:
                        file_abs_path = os.path.join(self.now_dir_path,item)
                        # print(file_abs_path  )
                        if os.path.isfile(file_abs_path) :
                            #print(item,"文件")
                            data["file"].append(item)
                        else:
                            #print(item,"文件夹")
                            data["dir"].append(item)
                    #print(data)
                    self.send_response(260,data)
                    print("发送文件列表成功！")
                else:
                    print(settings.STATUS_CODE[261])
                    self.send_response(261)
            else:
                print(settings.STATUS_CODE[262])
                self.send_response(262)
        else:
            print("用户没有通过验证，没有权限！")
    def _cd(self, *args, **kwargs):
        if self.__auth_flag :
            data = args[0]
            print(data)
            if data.get("cd_dir") == "\\":  #切换到根目录（个人主页目录）
                self.now_dir_path = self.user_home_dir
            elif data.get("cd_dir") == "..":    #切换到上一级目录
                if self.now_dir_path != self.user_home_dir:
                    path_list = self.now_dir_path.split("\\")
                    del path_list[-1]
                    self.now_dir_path = "\\".join(path_list[0:])
                else:
                    data["now_dir_path"] = self.now_dir_path
                    self.send_response(264, data)
                    return
            elif data.get("cd_dir") == "":
                pass
            else:
                path_list = self.now_dir_path.split("\\")
                path_list.append(data.get("cd_dir"))
                dir_path = "\\".join(path_list )
                if os.path.exists(dir_path):
                    self.now_dir_path = dir_path
                else:
                    data["now_dir_path"] = self.now_dir_path
                    self.send_response(262, data)
            data["now_dir_path"] = self.now_dir_path
            print(data)
            self.send_response(263,data)
            print(settings.STATUS_CODE[263])
        else:
            print("用户没有通过验证，没有权限！")

