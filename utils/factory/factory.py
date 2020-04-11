# -*- coding: utf-8 -*-
from entity.relation import ResultDBConfig, MysqlHostConfig, SqlServerConfig
import utils
import re
import configparser

logger = utils.root_logger


#  对config中设置的文件配置进行解析，将值赋值给实体类
class ParseConfig:
    @staticmethod
    def get_config_dict(cfg_mapping, file):
        # 配置文件解析器
        config = configparser.ConfigParser()
        config.read(file)  # 读取配置文件
        content = config['default'] # content可看成配置的字典
        ipdirs = {}
        for key in content:  # 循环对配置的key和value进行读取
            if re.match('.*ips\Z', key):  # 10.1.72.6~8:22,10.1.72.10:22  # 检测配置文件中的host_ips值是否符合此样例
                if not re.match(r'(\d+\.\d+\.\d+\.\d+(~\d+)?:\d+,?)+',content[key]):
                    logger.error(f'config of iplist is {content[key]} should be same as \n'
                                 f'e.g   10.1.72.6~8:22,10.1.72.10:22')
                    raise ValueError
                else:  # 对host_ips进行解析并生产 ip:port的字典，并将此字典赋值给配置字典cfg_mapping
                    cfg_mapping[key] = ParseConfig.get_ip_lists(ipdirs, content[key])
            else:  # 除host_ip之外的key处理
                cfg_mapping[key] = content[key]
        logger.info(f'information of config is dict {cfg_mapping}')
        return cfg_mapping

    @staticmethod
    def get_ip_lists(ipdirs, ip_ports):
        if ip_ports == '':
            logger.error('ip information is null')
        else:  # 10.1.72.6~10:22,10.1.72.13:22
            ip_lists = ip_ports.split(',')  # ip列表是有逗号进行区分
            for i in range(len(ip_lists)):
                res = re.match(r'(.*\d+\.)+(\d+)~(\d+):(\d+)', ip_lists[i])
                if res:  # 对ip已区间设置的进行解析
                    for inc in range(int(res.group(2)), int(res.group(3)) + 1):
                        mid_ip = res.group(1) + str(inc)
                        ipdirs[mid_ip] = res.group(4)
                else:
                    ip, port = ip_lists[i].split(':')
                    ipdirs[ip] = port
        return ipdirs


class GenerateBeanFactory:
    cfg_mapping = {}

    @classmethod
    def createConfigBean(cls, file):
        cls.cfg_mapping.clear()
        cls.cfg_mapping = ParseConfig.get_config_dict(cls.cfg_mapping, file)


class MysqlBeanFactory(GenerateBeanFactory):

    @classmethod
    def createConfigBean(cls, file):
        logger.info(f'mysql factory create parseBean by file {file}')
        super(MysqlBeanFactory,cls).createConfigBean(file)
        cls.cfg_mapping['name'] = 'mysql'
        return MysqlHostConfig(**cls.cfg_mapping)


class SqlServerBeanFactory(GenerateBeanFactory):
    @classmethod
    def createConfigBean(cls, file):
        logger.info(f'sqlserver factory create parseBean by file {file}')
        super(SqlServerBeanFactory,cls).createConfigBean(file)
        cls.cfg_mapping['name'] = 'sqlserver'
        return SqlServerConfig(**cls.cfg_mapping)


class ResultDBBeanFactory(GenerateBeanFactory):
    @classmethod
    def createConfigBean(cls, file):
        logger.info(f'resultdb factory create parseBean by file {file}')
        super().createConfigBean(file)
        cls.cfg_mapping['name'] = 'resultdb'
        return ResultDBConfig(**cls.cfg_mapping)


if __name__ == '__main__':
    logger.info('start produce')
    mysqlConfigBean = MysqlBeanFactory.createConfigBean(utils.mysql_cfg_path)
    sqlserverConfigBean = SqlServerBeanFactory.createConfigBean(utils.sqlserver_cfg_path)
    resultDBBean = ResultDBBeanFactory.createConfigBean(utils.resultdb_cfg_path)
    print(resultDBBean)
