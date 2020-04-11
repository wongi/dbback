# -*- coding: utf-8 -*-
import fnmatch
import utils
from utils.factory import factory
import os

logger = utils.get_logger()

config = 'configs'
mysqlbak = 'mysql'
sqlserver = 'sqlserver'
resultdb = 'result_db'
linux_port = ['22']
window_port = ['3389']

class Proceed:
    # 1、读取配置文件列表，按照配置文件产生configbean
    config_list = []  # 配置文件
    config_database_bean_list = []  # 备份数据库的configbeans
    config_db_result = None  # 结果存储实例的configbean
    cfg_path = utils.root_path + os.sep + config + os.sep  # config path

    @classmethod
    def get_config_bean(cls):
        if len(cls.config_list) > 0:
            logger.info('now creating config bean by factory')
            for file in cls.config_list:
                if os.path.basename(file).startswith(mysqlbak):
                    cls.config_database_bean_list.append(factory.MysqlBeanFactory.createConfigBean(utils.mysql_cfg_path))
                if os.path.basename(file).startswith(sqlserver):
                    cls.config_database_bean_list.append(factory.SqlServerBeanFactory.createConfigBean(utils.sqlserver_cfg_path))
                if os.path.basename(file).startswith(resultdb):
                    config_db_result = factory.ResultDBBeanFactory.createConfigBean(utils.resultdb_cfg_path)
        else:
            logger.error('config lists is null')

    @classmethod
    def get_config(cls):
        for filename in os.listdir(cls.cfg_path):
            if fnmatch.fnmatch(filename, '*_cfg.ini'):
                cls.config_list.append(cls.cfg_path + filename)
        if cls.config_list:
            logger.info(f'These configs are given {cls.config_list}')
            cls.get_config_bean()
        else:
            logger.error(f'There are not any configs matched under the path {cls.cfg_path}')
            raise FileNotFoundError

    # 2、对config中的flag进行确认，3个数值，第一个表示备份，第二个表示检测，第三个表示异地存储，1表示开启，0表示关闭
    @classmethod
    def do_bak(cls, instance):
        pass

    @classmethod
    def do_check(cls, instance):
        pass

    @classmethod
    def do_store(cls, instance):
        pass

    @classmethod
    def do_proceed(cls, instance):
        bak_flag = 0
        check_flag = 0
        store_flag = 0
        if instance.host_proceed_flag[0:1] == '1':
            logger.info(f'{instance.name} proceed backup ')
            cls.do_bak(instance)
        if instance.host_proceed_flag[1:2] == '1':
            logger.info(f'{instance.name} proceed check ')
            cls.do_check(instance)
        if instance.host_proceed_flag[2:3] == '1':
            logger.info(f'{instance.name} proceed store ')
            cls.do_store(instance)

    @classmethod
    def proceed(cls):
        for instance in cls.config_database_bean_list:
            cls.do_proceed(instance)

    # 对各个ip列表进行逻辑处理，分为windows、linux

    # 3、备份处理

    # 4、备份检测

    # 5、异地存储

    # 6、数据库存储

    pass


if __name__ == '__main__':
    p = Proceed()
    p.get_config()
    p.proceed()