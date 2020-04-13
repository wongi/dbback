# -*- coding: utf-8 -*-
from enum import Enum
import paramiko
import utils
import winrm
from  utils.connhosts import linuxcmd,wincmd

logger = utils.get_logger()


class Param(Enum):
    W = 1
    R = 2
    CRONTAB_ADD = 'crontab -e '
    CRONTAB_LIS = 'crontab -l '
    MKDIR = 'mkdir '
    GREP = 'grep '
    CP = 'cp '


# windos连接方式和linux连接方式
class ConnectHost:
    _ip = None
    _port = None
    _user = None
    _pass = None

    def __init__(self, ip, port, user, pas):
        self._ip = ip
        self._port = port
        self._user = user
        self._pass = pas

    @property
    def port(self):
        return self._port

    @property
    def ip(self):
        return self._ip

    @property
    def user(self):
        return self._user

    def __str__(self):
        return f'Parameters in ConnectHost are [ip:{self._ip}, port:{self._port}, user:{self._user}]'

    def getConnectHost(self):  # 获取连接
        pass

    def getSCPConnect(self):  # 获取scp连接
       pass

    def closeConnectHost(self, conn):  # 关闭连接
        if conn:
            conn.close()
        else:
            logger.error('The connection is null')
            raise ConnectionError


class ConnectWindos(ConnectHost):

    def getConnectHost(self):
        try:
            print(f'http://{self._ip}:{self._port}/wsman,{self._user},{self._pass}')
            win_conn = winrm.Session(f'http://{self._ip}:{self._port}/wsman', auth=(self._user, self._pass))
            return win_conn
        except ConnectionRefusedError as e:
            logger.error(f'拒绝连接 {e}')
            raise ConnectionError
        except ConnectionAbortedError as e:
            logger.error(f'连接终止 {e}')
            raise ConnectionError


class ConnectUnix(ConnectHost):

    def getConnectHost(self):
        s=paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            s.connect(hostname=self._ip, port=self.port, username=self._user, password=self._pass, timeout=3)
            logger.info(f'login in {self._ip}')
        except ConnectionRefusedError as e:
            logger.error(f'拒绝连接 {e}')
            raise ConnectionError
        except ConnectionAbortedError as e:
            logger.error(f'连接终止 {e}')
            raise ConnectionError
        return s

    def getSCPConnect(self):
        # 创建ssh访问
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        ssh.connect(hostname=self._ip, port=self.port, username=self._user, password=self._pass, timeout=3)  # 远程访问的服务器信息

        # 创建scp
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        return sftp


if __name__ == '__main__':
    # unix_conn = ConnectUnix('10.1.72.12', '22', 'root', 'Wu*123456') #连接linux测试并传输文件
    # conn = unix_conn.getSCPConnect()
    # result = linuxcmd.exec_scp(conn, Param.R, '/root/test.sh', '/Users/threeboys33/tools/backup_check/test.sh')
    win_conn = ConnectWindos('10.1.133.40', '5985', 'Administrator', 'GJYX@126.com').getConnectHost() # 连接windows传输文件测试
    result = wincmd.exec_cmd(win_conn,r'C:\Windows\pscp.exe -batch -pw Chen5223335 D:\backup\test.dif.bak Threeboys33@10.32.82.176:/Users/threeboys33/tools/test/Users/threeboys33/tools/backup_check')
    print(result)
