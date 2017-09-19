

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import socketserver
from conf import settings
from core.ftp_server import FTPHandler





if __name__ == "__main__":
    print("启动服务器".center(50, "-"))
    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((settings.HOST, settings.PORT), FTPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()



