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
        self.host_ips = kwargs.get('host_ips')
        self.host_login_user,self.host_login_pass = self.get_user_pass(kwargs.get('host_login_info'))

    @staticmethod  # 确认数据库服务器的操作系统环境
    def get_host_system():

        pass


#  明细汇聚的数据库的配置
@singleton
class ResultDBConfig(Config):
    db_type = ''  # 数据库类型
    db_name = ''  # 数据库库名
    tb_name = ''  # 数据库表名
    tb_user = ''  # 数据库用户
    tb_pass = ''  # 数据库密码

    def __init__(self, **kwargs):

        super().__init__(host_ips=kwargs.get('result_db_ips'), host_login_info=kwargs.get('result_db_login_info'))
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
    host_bak_time = ''         # 数据库服务器备份时间
    oss_bucket = ''            # 数据库相应的oss路径
    host_proceed_flag = 0   # 数据库对应的操作标志

    def __init__(self, **kwargs):
        super().__init__(host_ips=kwargs.get('host_ips'), host_login_info=kwargs.get('host_login_info'))
        self.host_bak_script_file = kwargs.get('host_bak_script_file')
        self.host_bak_dir_name = kwargs.get('host_bak_dir_name')
        self.host_bak_log_name = kwargs.get('host_bak_log_name')
        self.host_bak_time = kwargs.get('host_bak_time')
        self.oss_bucket = kwargs.get('oss_bucket')
        self.host_proceed_flag = kwargs.get('host_proceed_flag')


#  mysql数据库服务器的配置
@singleton
class MysqlHostConfig(HostConfig):
    def __init__(self, **kwargs):
        super().__init__(host_ips=kwargs.get('mysql_host_ips'),
                         host_login_info=kwargs.get('mysql_host_login_info'),
                         host_bak_script_file=kwargs.get('mysql_host_bak_script_file'),
                         host_bak_dir_name=kwargs.get('mysql_host_bak_dir_name'),
                         host_bak_log_name=kwargs.get('mysql_host_bak_log_name'),
                         host_bak_time=kwargs.get('mysql_host_bak_time'),
                         oss_bucket=kwargs.get('mysql_oss_bucket'),
                         host_proceed_flag = kwargs.get('mysql_host_proceed_flag'))

    def __str__(self):
        return f'host_ips:{self.host_ips} \n' \
               f'host_login_user:{self.host_login_user} \n' \
               f'host_login_pass:{self.host_login_pass} \n' \
               f'host_bak_script_file:{self.host_bak_script_file} \n' \
               f'host_bak_dir_name:{self.host_bak_dir_name} \n' \
               f'host_bak_log_name:{self.host_bak_log_name} \n' \
               f'oss_bucket:{self.oss_bucket} \n' \
               f'host_proceed_flag:{self.host_proceed_flag}'


#  sqlserver数据服务器的配置
@singleton
class SqlServerConfig(HostConfig):

    sqlserver_db_bakmeta_tb = ''
    sqlserver_db_login_user = ''
    sqlserver_db_login_pass = ''

    def __init__(self, **kwargs):
        super().__init__(host_ips=kwargs.get('sqlserver_host_ips'),
                         host_login_info=kwargs.get('sqlserver_host_login_info'),
                         host_bak_script_file=kwargs.get('sqlserver_host_bak_script_file'),
                         host_bak_dir_name=kwargs.get('sqlserver_host_bak_dir_name'),
                         host_bak_log_name=kwargs.get('sqlserver_host_bak_log_name'),
                         host_bak_time=kwargs.get('sqlserver_host_bak_time'),
                         oss_bucket=kwargs.get('sqlserver_oss_bucket'),
                         host_proceed_flag = kwargs.get('sqlserver_host_proceed_flag'))
        self.sqlserver_db_bakmeta_tb = kwargs.get('sqlserver_db_bakmeta_tb')
        self.sqlserver_db_login_user, self.sqlserver_db_login_pass = super().get_user_pass(kwargs.get('sqlserver_db_login_info'))

    def __str__(self):
        return f'host_ips:{self.host_ips} \n' \
               f'host_login_user:{self.host_login_user} \n' \
               f'host_login_pass:{self.host_login_pass} \n' \
               f'host_bak_script_file:{self.host_bak_script_file} \n' \
               f'host_bak_dir_name:{self.host_bak_dir_name} \n' \
               f'host_bak_log_name:{self.host_bak_log_name} \n' \
               f'oss_bucket:{self.oss_bucket} \n' \
               f'host_proceed_flag:{self.host_proceed_flag} \n' \
               f'sqlserver_db_bakmeta_tb:{self.sqlserver_db_bakmeta_tb} \n' \
               f'sqlserver_db_login_user:{self.sqlserver_db_login_user} \n' \
               f'sqlserver_db_login_pass:{self.sqlserver_db_login_pass} \n'

