from enum import Enum
import logging
import logging.config
import os
from datetime import datetime


#  枚举变量
class Param(Enum):
    LINUX = 0
    WINDOWS = 1
    MYSQL = 2
    SQLSERVER = 3
    ORACLE = 4
    POSTGRES = 5


# 项目跟路径和配置文件名称
cfg_path = 'configs'
root_path = os.path.abspath(os.path.dirname(__file__))[ : os.path.abspath(os.path.dirname(__file__)).find('dbback') + len('dbback')]
log_cfg_path = root_path + os.path.sep + cfg_path + os.path.sep + 'log.conf'
mysql_cfg_path = root_path + os.path.sep + cfg_path + os.path.sep + 'mysql_cfg.ini'
sqlserver_cfg_path = root_path + os.path.sep + cfg_path + os.path.sep + 'sqlserver_cfg.ini'
resultdb_cfg_path = root_path + os.path.sep + cfg_path + os.path.sep + 'result_db_cfg.ini'
scripts_path = root_path + os.path.sep + 'scripts' + os.path.sep + os.path.sep

# 日志全局配置
def get_logger(name=''):
    logging.config.fileConfig(log_cfg_path)
    if name == '':
        return logging.getLogger()
    else:
        return logging.getLogger(name)


root_logger = get_logger()
file_logger = get_logger('logfile')


# 检测文件是否存在
def check_file_exists(file):
    if not os.path.isfile(file):
        root_path.error(f'The file {file} does not exists')
        raise FileNotFoundError


# 执行时常
def timer(func):
  def wrapper(*args, **kw):
    fstr='%Y-%m-%d %H:%M:%S'
    start_time=datetime.now()
    # 这是函数真正执行的地方
    func(*args, **kw)
    end_time=datetime.now()
    cost_time = (end_time - start_time).seconds
    if cost_time == 0:
        cost_time = '0.'+ str((end_time - start_time).microseconds)[0 : 2]
    root_logger.info(f'开始：{start_time.strftime(fstr)}, 结束：{end_time.strftime(fstr)}, 花费：{cost_time}s')
  return wrapper


local_ip = 'localhost'