# -*- coding: utf-8 -*-
import fnmatch
import utils
import re
from datetime import datetime
from utils.factory import factory
from utils.connhosts import ConnectUnix, ConnectWindos, linuxcmd, wincmd,Param
import os
from entity.relation import Result
from crontab import CronTab,CronItem

logger = utils.get_logger()

config = 'configs'
mysqlbak = 'mysql'
sqlserver = 'sqlserver'
resultdb = 'result_db'
linux_port = ['22']
window_port = ['3389']

crontab_str='echo date >> ~/time.log'
crontab_time = 7
crontab_comment = 'database backup task'
crontab_flag=False
crontab_user = 'threeboys33'

time = datetime.now()
date_time = time.strftime('%Y%m%d')

def config_crontab(crontab_user, instance):
    global crontab_flag
    crontab_str.strip('\n')
    # 检测本地机器是否有定时任务设置
    if crontab_time:
        user_cron = CronTab(crontab_user)
        crons = user_cron.crons

        for item in crons:
            if crontab_str in str(item):
                crontab_flag = True
                break

        if crontab_flag == False:
            item = user_cron.new(crontab_str, crontab_comment, crontab_user)
            item.setall(f'0 {instance.host_bak_time} * * *')
            user_cron.write()
        else:
            for task in user_cron:
                if task.comment == crontab_comment and task.hour != instance.host_bak_time:
                    task.setall(f'0 {instance.host_bak_time} * * *')
                    user_cron.write()


def get_script_file(name):
    for i in os.listdir(utils.scripts_path):
        if fnmatch.fnmatch(f'{name}.*', i):
            return utils.scripts_path + os.sep + i


# 通过结果实例Result的参数在linux进行备份
def linux_bak(r, k, v, instance):
    # 当bak——time不为null时，检测本地机器是否有定时任务设置,没有则添加上，如果时间又变化修改时间
    config_crontab(crontab_user, instance)

    logger.info(f'开始获取{k}的连接实例')
    linux = ConnectUnix(k, v, instance.host_login_user, instance.host_login_pass)
    login_conn = linux.getConnectHost()
    scp_conn = linux.getSCPConnect()
    # 判定目录是不是存在，不存在创建
    logger.info('check ')
    res = linuxcmd.check_file_exists(instance.host_bak_script_file,login_conn)
    linuxcmd.check_dir_exists(instance.host_bak_file_dir_name,True, login_conn)
    linuxcmd.check_dir_exists(instance.host_bak_log_dir_name, True, login_conn)
    # 如果时间设置不为null，判定定时任务是否开启，没有开启的话，开启任务
    # 如果时间设置为null, 手动备份
    # 检测备份结果，并设置状态，或者异常信息
    if res == 'False':
        dir_path = os.path.dirname(instance.host_bak_script_file)
        linuxcmd.check_dir_exists(dir_path, True, login_conn)
        bak_file = get_script_file(instance.name)
        logger.info(f'传输{instance.host_bak_script_file}至 {k} 服务器')
        linuxcmd.exec_scp(scp_conn, Param.W, bak_file, instance.host_bak_script_file)

    sh_cmd = linuxcmd.scripts_command(instance.host_bak_script_file)
    sh_res = linuxcmd.exec_cmd(login_conn, sh_cmd)

    # ls root/mysql/backup/data | grep -E full_mysql_.*} | grep date_time
    ls_bak_file_cmd = f'ls {instance.host_bak_file_dir_nam} | grep -E {instance.host_bak_file_name} | grep {date_time} | wc -l'
    ls_bak_file_res = linuxcmd.exec_cmd(login_conn, ls_bak_file_cmd)

    ls_bak_log_cmd = f'ls {instance.host_bak_log_dir_name} | grep -E {instance.host_bak_log_name} | grep {date_time}'
    ls_bak_log_res = linuxcmd.exec_cmd(login_conn, ls_bak_file_cmd).strip('\n')

    cat_bak_log_cmd = f'grep -in error {instance.host_bak_log_dir_name}/{ls_bak_file_res}'

    # ls root/mysql/backup/logs | grep -E full_log_\d{6} | grep data_time | grep -in error
    cat_bak_log_cmd = f'grep -in error {instance.host_bak_log_dir_nam}'

    print(str)


# 通过结果实例Result的参数在windows进行备份
def window_bak(r, k, v, instance):
    pass


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

    # 3、备份处理
    @classmethod
    def do_bak(cls, instance):
        # 判断端口22为linux 3389windows
        for k, v in instance.host_ips.items():
            # 构造检测实例
            r = Result(utils.local_ip, k, instance.name)
            r.bak_meta_tb = instance.bak_meta_tb
            r.bak_file_name = instance.bak_file_name
            r.bak_script_file = instance.host_bak_script_file
            r.bak_dir_name = instance.host_bak_file_dir_name
            r.bak_dir_log = instance.host_bak_log_dir_name
            r.bak_frequency = instance.host_bak_time
            if v in linux_port:
                linux_bak(r, k, v, instance)
                pass
            elif v in window_port:
                window_bak(r, k, v, instance)
        pass

    # 4、备份检测
    @classmethod
    def do_check(cls, instance):
        # 判断端口22为linux 3389windows
        # 判断实例的各个ip的对应结果实例是否为null，为null则进行检测，不为则进行检测
        # 条件（是否有备份文件生成，或者表是不是有备份记录）
        pass

    # 5、异地存储
    @classmethod
    def do_store(cls, instance):
        # 对各个ip列表进行逻辑处理，分为windows、linux
        # 回传文件至本地
        # 判定ossbucket是不是存在
        # 上传备份文件至bucket
        pass

    # 2、对config中的flag进行确认，3个数值，第一个表示备份，第二个表示检测，第三个表示异地存储，1表示开启，0表示关闭
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

    # 6、数据库存储

    pass


if __name__ == '__main__':
    p = Proceed()
    p.get_config()
    p.proceed()