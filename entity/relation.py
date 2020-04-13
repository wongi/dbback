#  -*- coding: utf-8 -*-
import utils
logger = utils.get_logger()

instances = {}


def singleton(cls):  # 配置文件单例装饰器
    def get_instance(*args, ** kwargs):
        cls_name = cls.__name__
        if not cls_name in instances:
            instance = cls(*args, **kwargs)
            instances[cls_name] = instance
        return instances[cls_name]
    return get_instance


#  每个数据库的配置都有对应的ip信息和地址，抽取成父类Config
class Config:
    name = ''
    host_ips = []         # 数据库服务其实例IP列表
    host_login_user = ''  # 数据库服务器登陆用户信息 user/pass
    host_login_pass = ''

    @staticmethod  # 将密码和用户进行解析
    def get_user_pass(login_info):
        if login_info:
            return str(login_info).split('/')
        else:
            logger.error('user/password is null')
            raise ValueError

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.host_ips = kwargs.get('host_ips')
        self.host_login_user,self.host_login_pass = self.get_user_pass(kwargs.get('host_login_info'))

    def __getattr__(self, item):
        return '-'

#  明细汇聚的数据库的配置
@singleton
class ResultDBConfig(Config):
    db_type = ''  # 数据库类型
    db_name = ''  # 数据库库名
    tb_name = ''  # 数据库表名
    tb_user = ''  # 数据库用户
    tb_pass = ''  # 数据库密码

    def __init__(self, **kwargs):

        super().__init__(name=kwargs.get('name'), host_ips=kwargs.get('result_db_ips'), host_login_info=kwargs.get('result_db_login_info'))
        self.db_type = kwargs.get('result_db_type')
        self.db_name = kwargs.get('result_db_name')
        self.tb_name = kwargs.get('result_db_tbname')
        self.tb_user = self.host_login_user
        self.tb_pass = self.host_login_pass

    def __str__(self):
        return f'host_ips:{self.host_ips} \n' \
               f'host_login_user:{self.host_login_user} \n' \
               f'host_login_pass:{self.host_login_pass} \n' \
               f'db_type:{self.db_type} \n' \
               f'tb_name:{self.tb_name} \n' \
               f'db_name:{self.db_name} \n'


#  数据服务器的配置
class HostConfig(Config):
    host_bak_script_file = ''  # 数据库服务器备份脚本
    host_bak_dir_name = ''     # 数据库服务器备份路径
    host_bak_log_name = ''     # 数据库服务器备份日志
    host_bak_log_name = ''     # 数据库服务器备份正则
    host_bak_time = ''         # 数据库服务器备份时间
    oss_bucket = ''            # 数据库相应的oss路径
    host_proceed_flag = 0   # 数据库对应的操作标志

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('name'), host_ips=kwargs.get('host_ips'), host_login_info=kwargs.get('host_login_info'))
        self.host_bak_script_file = kwargs.get('host_bak_script_file')
        self.host_bak_file_dir_name = kwargs.get('host_bak_file_dir_name')
        self.host_bak_file_name = kwargs.get('host_bak_file_name')
        self.host_bak_log_dir_name = kwargs.get('host_bak_log_dir_name')
        self.host_bak_log_name = kwargs.get('host_bak_log_name')
        self.host_bak_time = kwargs.get('host_bak_time')
        self.oss_bucket = kwargs.get('oss_bucket')
        self.host_proceed_flag = kwargs.get('host_proceed_flag')


#  mysql数据库服务器的配置
@singleton
class MysqlHostConfig(HostConfig):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('name'),
                         host_ips=kwargs.get('mysql_host_ips'),
                         host_login_info=kwargs.get('mysql_host_login_info'),
                         host_bak_script_file=kwargs.get('mysql_host_bak_script_file'),
                         host_bak_file_dir_name=kwargs.get('mysql_host_bak_file_dir_name'),
                         host_bak_file_name=kwargs.get('mysql_host_bak_file_name'),
                         host_bak_log_dir_name=kwargs.get('mysql_host_bak_log_dir_name'),
                         host_bak_log_name=kwargs.get('mysql_host_bak_log_name'),
                         host_bak_time=kwargs.get('mysql_host_bak_time'),
                         oss_bucket=kwargs.get('mysql_oss_bucket'),
                         host_proceed_flag=kwargs.get('mysql_host_proceed_flag'))

    def __str__(self):
        return f'name:{self.name} \n' \
               f'host_ips:{self.host_ips} \n' \
               f'host_login_user:{self.host_login_user} \n' \
               f'host_login_pass:{self.host_login_pass} \n' \
               f'host_bak_script_file:{self.host_bak_script_file} \n' \
               f'host_bak_file_dir_name:{self.host_bak_file_dir_name} \n' \
               f'host_bak_file_name:{self.host_bak_file_name} \n' \
               f'host_bak_log_dir_name:{self.host_bak_log_dir_name} \n' \
               f'host_bak_log_name:{self.host_bak_log_name} \n' \
               f'oss_bucket:{self.oss_bucket} \n' \
               f'host_proceed_flag:{self.host_proceed_flag} \n'


#  sqlserver数据服务器的配置
@singleton
class SqlServerConfig(HostConfig):

    sqlserver_db_bakmeta_tb = ''
    sqlserver_db_login_user = ''
    sqlserver_db_login_pass = ''

    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('name'),
                         host_ips=kwargs.get('sqlserver_host_ips'),
                         host_login_info=kwargs.get('sqlserver_host_login_info'),
                         host_bak_script_file=kwargs.get('sqlserver_host_bak_script_file'),
                         host_bak_file_dir_name=kwargs.get('sqlserver_host_bak_file_dir_name'),
                         host_bak_file_name=kwargs.get('sqlserver_host_bak_file_name'),
                         host_bak_log_dir_name=kwargs.get('sqlserver_host_bak_log_dir_name'),
                         host_bak_log_name=kwargs.get('sqlserver_host_bak_log_name'),
                         host_bak_time=kwargs.get('sqlserver_host_bak_time'),
                         oss_bucket=kwargs.get('sqlserver_oss_bucket'),
                         host_proceed_flag = kwargs.get('sqlserver_host_proceed_flag'))
        self.sqlserver_db_bakmeta_tb = kwargs.get('sqlserver_db_bakmeta_tb')
        self.sqlserver_db_login_user, self.sqlserver_db_login_pass = super().get_user_pass(kwargs.get('sqlserver_db_login_info'))

    def __str__(self):
        return f'name:{self.name} \n' \
               f'host_ips:{self.host_ips} \n' \
               f'host_login_user:{self.host_login_user} \n' \
               f'host_login_pass:{self.host_login_pass} \n' \
               f'host_bak_script_file:{self.host_bak_script_file} \n' \
               f'host_bak_file_dir_name:{self.host_bak_file_dir_name} \n' \
               f'host_bak_file_name:{self.host_bak_file_name} \n' \
               f'host_bak_log_dir_name:{self.host_bak_log_dir_name} \n' \
               f'host_bak_log_name:{self.host_bak_log_name} \n' \
               f'oss_bucket:{self.oss_bucket} \n' \
               f'host_proceed_flag:{self.host_proceed_flag} \n' \
               f'sqlserver_db_bakmeta_tb:{self.sqlserver_db_bakmeta_tb} \n' \
               f'sqlserver_db_login_user:{self.sqlserver_db_login_user} \n' \
               f'sqlserver_db_login_pass:{self.sqlserver_db_login_pass} \n'


class Result(object):  # 待修正
    local_ip = ''
    host_ip = ''
    db_type = ''
    bak_db_flag = -1
    bak_check_flag = -1
    bak_store_flag = -1
    bak_meta_tb = ''
    bak_file_name = ''
    bak_file_size = '0m'
    bak_total_sum = 0
    bak_total_size = '0m'
    bak_script_file = ''
    bak_dir_name = ''
    bak_dir_log = ''
    bak_time = 0
    bak_strategy = ''
    bak_oss_bucket = ''
    bak_sys_used = 0
    error_code = 1
    error_msg = ''
    check_time = ''

    def __init__(self, local_ip, host_ip, db_type):  # 初始化每个ip实例的instance
        self.local_ip = local_ip
        self.host_ip = host_ip
        self.db_type = db_type

    def __str__(self):
        return f'local_ip:{self.local_ip} \n' \
               f'host_ip:{self.host_ip} \n' \
               f'db_type:{self.db_type} \n' \
               f'bak_db_flag:{self.bak_db_flag} \n' \
               f'bak_check_flag:{self.bak_check_flag} \n' \
               f'bak_store_flag:{self.bak_store_flag} \n' \
               f'bak_meta_tb:{self.bak_meta_tb} \n' \
               f'bak_file_name:{self.bak_file_name} \n' \
               f'bak_file_size:{self.bak_file_size} \n' \
               f'bak_total_sum:{self.bak_total_sum} \n' \
               f'bak_total_size:{self.bak_total_size} \n' \
               f'bak_script_name:{self.bak_script_file} \n' \
               f'bak_dir_name:{self.bak_dir_name} \n' \
               f'bak_dir_log:{self.bak_dir_log} \n' \
               f'bak_time:{self.bak_time} \n' \
               f'bak_strategy:{self.bak_strategy} \n' \
               f'bak_oss_bucket:{self.bak_oss_bucket} \n' \
               f'bak_sys_used:{self.bak_sys_used} \n' \
               f'error_code:{self.error_code} \n' \
               f'error_msg:{self.error_msg} \n' \
               f'check_time:{self.check_time} \n'


if __name__ == '__main__':
    c = Config(name='test', host_ips='10.1.72.6:22', host_login_info='root/Wu*123456')
    print(c.bak_meta_tb)