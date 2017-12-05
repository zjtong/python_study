# -*- coding: utf-8 -*-
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)
import json,pickle,threading


class Host_Manage():
    '''
    主机管理系统接口
    '''
    def __init__(self,SSH_Manage_Obj):
        '''
        构造函数
        '''
        self.SSH = SSH_Manage_Obj
        self.DB_PATH = self.SSH.DB_PATH
        self.Main_Menu()


    def Main_Menu(self):
        # 显示菜单
        group_name = self.Show_Menu()
        # 获取主机组下的主机信息字典
        host_dict = self.Get_Host_Dict(group_name)
        # 显示机组控制菜单
        self.Show_Host_Menu(group_name, host_dict)

    def Show_Menu(self):
        '''
        显示菜单
        :return:返回选择的主机组名
        '''
        print(' 选择主机群组 '.center(40,'-'))
        self.Group_List = self.Get_Host_Group()
        if len(self.Group_List) == 0:
            print('\t\033[31;1m机组数量为零，请创建机组继续...\033[0m')
            self.Create_Group()
        else:
            count = 1
            for group_name in self.Group_List:
                print("\t\t",count,'.',group_name)
                count += 1
            while True:
                act = input('请选择主机组(q退出，add新增机组)：').strip()
                if act.lower() == 'q':
                    exit()
                elif act.lower() == 'add':
                    self.Create_Group()
                elif act.isdigit() and int(act) < len(self.Group_List)+1:
                    return self.Group_List[int(act)-1]
                else:
                    print('选择错误！')
                    # continue

    def Get_Host_Group(self):
        '''
        获取主机组
        :return: 返回主机组列表
        '''
        groupname_list = []
        filename = os.path.join(self.DB_PATH,'groupname_list.json')
        if os.path.isfile(filename):
            with open(filename,'r') as f:
                groupname_list = json.load(f)
        else:
            with open(filename,'w') as f:
                json.dump(groupname_list,f)
        return groupname_list

    def Show_Host_Menu(self,group_name,host_dict):
        '''
        主机管理菜单
        :param group_name: 机组名
        :param host_dict: 主机信息字典
        :return:
        '''

        menu = '''---------------- 主机管理菜单 ----------------
        1. 执行命令
        2. 上传/下载
        3. 新增主机
        4. 修改主机信息'''
        menu_dic = {
            "1": self.Run_Command,
            "2": self.FTP_File,
            "3": self.Add_Host,
            "4": self.Modify_Host,
        }
        while True:
            print(menu)
            choice = input("请选择(q退出）>>>:").strip().lower()
            if choice in menu_dic:
                menu_dic[choice](group_name,host_dict)
            elif choice == "q":
                exit()
            else:
                print('\033[31;1m选择错误!请重新输入...\033[0m')

    def Run_Command(self,group_name,host_dict):
        '''
        执行命令
        :param host_dict: 主机信息字典
        :return:
        '''
        self.Show_Host_Info(group_name,host_dict)
        while True:
            print('在机组执行命令(q退出)'.center(50,'-'))
            cmd = input('请输入命令(linux)>>>:').strip().lower()
            if cmd == 'q':
                break
            else:
                #print(host_dict)
                # break
                tread_list=[]
                for host in host_dict:
                    host_tread = threading.Thread(
                        target=self.SSH.Create_SSHClient,
                        args=(host_dict[host]['ip'],int(host_dict[host]['port']),host_dict[host]['user'],host_dict[host]['pwd'],cmd)
                    )
                    tread_list.append(host_tread)
                    host_tread.start()
                for t in tread_list:
                    t.join()
                continue

        self.Main_Menu()

    def FTP_File(self,group_name,host_dict):
        '''
        上传下载文件
        :param group_name:
        :param host_dict:
        :return:
        '''
        self.Show_Host_Info(group_name, host_dict)
        print('命令帮助'.center(50,'-'))
        print('上传文件：put local_file host_file')
        print('下载文件：get host_file local_file')
        print('-'*50)
        while True:
            act = input('请输入命令（q退出）：').strip().lower()
            if act.lower() == 'q':
                break
            else:
                cmd_list = act.split()
                if len(cmd_list) !=3:
                    print('命令错误！')
                    continue
                else:
                    if cmd_list[0].lower() == 'put':
                        cmd_dict = {
                            'act': 'upload',
                            'local_file':cmd_list[1],
                            'host_file': cmd_list[2]
                        }

                    elif cmd_list[0].lower() == 'get':
                        cmd_dict = {
                            'act': 'download',
                            'local_file': cmd_list[2],
                            'host_file': cmd_list[1]
                        }

                    else:
                        print('命令错误！')
                        continue
                tread_list =[]
                for host in host_dict:
                    host_tread = threading.Thread(
                        target=self.SSH.Create_SSHFTP,
                        args=(host_dict[host]['ip'], int(host_dict[host]['port']), host_dict[host]['user'],
                              host_dict[host]['pwd'], cmd_dict)
                    )
                    tread_list.append(host_tread)
                    host_tread.start()
                for t in tread_list:
                    t.join()
                continue
        self.Main_Menu()




    def Add_Host(self,group_name,host_dict):
        '''
        在选定的主机组中新增主机
        :param host_dict: 主机信息字典
        :return:
        '''
        self.Create_Host(group_name)
        self.Main_Menu()



    def Modify_Host(self,group_name,host_dict):
        print('选择要修改的主机'.center(50,'-'))
        count = 0
        host_list = []
        for host in host_dict:
            host_list.append(host)
            print(count,'.',host, '(', host_dict[host]['ip'], ')')
            count += 1
        while True:
            act = input('请选择(q退出)：').strip().lower()
            if act.isdigit() and int(act)< len(host_list):
                self.Show_Host_Info(group_name,host_dict,host_list[int(act)])
                ip = input('输入主机地址：')
                port = input('输入主机端口：')
                user = input('输入主机用户名：')
                pwd = input('输入主机密码：')
                host_dict[host_list[int(act)]] = {
                    'ip': ip,
                    'port': port,
                    'user': user,
                    'pwd': pwd
                }
                # 写入数据
                host_file = os.path.join(self.DB_PATH,"%s.json"%group_name)
                with open(host_file, 'w') as f:
                    json.dump(host_dict, f)
                break
            elif act == 'q':
                break
            else:
                print('选择错误！')
        self.Main_Menu()


    def Show_Host_Info(self,group_name,host_dict,mode=''):
        '''
        显示主机信息
        :param group_name: 机组名称
        :param host_dict: 主机信息字典
        :param mode: 空为简显示，需要单个主机完整信息时mode为主机名称（用于修改主机信息）
        :return:
        '''
        if mode =='':
            print('主机组【%s】包含以下主机'.center(50, '-') % (group_name))
            for host in host_dict:
                print(host, '(', host_dict[host]['ip'], ')')
        else:
            if mode in host_dict:
                print('主机【%s】信息如下：'.center(50,'-') %mode)
                print('主机地址:',host_dict[mode]['ip'])
                print('SSH端口:', host_dict[mode]['port'])
                print('用户名:', host_dict[mode]['user'])
                print('密码:', host_dict[mode]['pwd'])
                print('-'*50)
            else:
                print('主机名称错误！')





    def Get_Host_Dict(self,group_name):
        '''
        根据主机组名称返回机组字典
        :param group_name: 主机组名称
        :return: host_dict
        '''
        host_dict = {}
        filename = os.path.join(self.DB_PATH,"%s.json"%group_name)
        # print(filename)
        if os.path.isfile(filename):
            with open(filename,'r')as f:
                host_dict = json.load(f)
        else:
            print('机组信息数据丢失！')
        return host_dict

    def Create_Group(self):
        '''
        新建机组
        :return:
        '''
        group_name = input('请输入新机组名：')
        if group_name in self.Group_List:
            print('此机组名已被创建')
            group_name =''
        else:
            self.Group_List.append(group_name)
            filename = os.path.join(self.DB_PATH, 'groupname_list.json')
            with open(filename,'w') as f:
                json.dump(self.Group_List,f)
            self.Create_Host(group_name)

    def Create_Host(self,group_name):
        '''
        向主机组group_name里添加主机信息
        :param group_name: 主机组名
        :return: 返回添加后此主机组中所有主机信息
        '''
        host_file = os.path.join(path,self.DB_PATH,"%s.json"%group_name)
        host_dict ={}
        if os.path.isfile(host_file):
            with open(host_file,'r') as f:
                host_dict = json.load(f)
        else:
            host_dict = {}
        flag = False
        while not flag:
            print('新增主机信息'.center(50, '-'))
            host_name = input('请输入主机名称：')
            if host_name in host_dict:
                print('此主机已被创建')
                continue
            ip = input('输入主机地址：')
            port = input('输入主机端口：')
            user = input('输入主机用户名：')
            pwd = input('输入主机密码：')
            host_dict[host_name] = {
                'ip':ip,
                'port':port,
                'user':user,
                'pwd':pwd
            }
            while True:
                act = input('是否继续创建主机(y/n)？').strip().lower()
                if act == 'y':
                    flag = False
                    break
                elif act == 'n':
                    flag = True
                    break
                else:
                    print('输入错误！')
                    continue
        # 写入数据
        with open(host_file, 'w') as f:
            json.dump(host_dict,f)
        return host_dict


