
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR )


USER_HOME = "%s\\home" % BASE_DIR
LOG_DIR =  "%s\\log" % BASE_DIR
LOG_LEVEL = "DEBUG"

ACCOUNT_FILE = "%s\\conf\\accounts.cfg" % BASE_DIR
ACCOUNT_DIR = "%s\\db" % BASE_DIR


HOST = "localhost"
PORT = 9999

#设计规范的状态码
STATUS_CODE  = {
    250 : "无效的命令格式, e.g: {'action':'get','filename':'test.py','size':344}",
    251 : "无效的命令！ ",
    252 : "Invalid auth data",
    253 : "用户名或密码错误！",
    254 : "Passed authentication",
    255 : "无效的文件名！",
    256 : "File doesn't exist on server",
    257 : "ready to send file",
    258 : "md5 verification",
    259 : "ready to receive file",
    260 : "发送文件列表成功...",
    261 : "目录为空！",
    262 : "目录不存在！",
    263 : "获取目录成功...",
    264 : "当前目录为根目录,无法返回上一级目录",
    265 : "准备接收文件...",
    266 : "最大接收数据大小，默认10mb，上传的文件太大",
    267 : "文件为空",
    268 : "",
    269 : "",
    270 : "",
    271 : "",
}


