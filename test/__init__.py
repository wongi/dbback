import configparser
import utils
import re

logger = utils.get_logger()

# 测试配置文件的读取
def test_config():
    config = configparser.ConfigParser()
    config.read(utils.mysql_cfg_path)
    content = config['default']
    print(type(content))
    mapping = dict()
    for key in content:
        mapping[key] = content[key]
    print(mapping)


# 测试ip列表的解析
def test_ipparse():
    ip='10.1.72.6~8:22'
    res = re.match(r'(.*\d+\.)+(\d+)~(\d+):(\d+)',ip)
    if res:
        logger.info(f'ip prefix is {res.group(1)}')
        logger.info(f'ip start is {res.group(2)}')
        logger.info(f'ip end is {res.group(3)}')
        logger.info(f'ip port is {res.group(4)}')
        for inc in range(int(res.group(2)), int(res.group(3)) + 1):
            midip = res.group(1) + str(inc)
            logger.info(f'ip midd is {midip}, port is {res.group(4)}')
    else:
        logger.error('not match')

    ipkeysuffxi = 'mysql_hosts_ips'
    sufres = re.match(r'.*ips\Z', ipkeysuffxi, re.IGNORECASE)
    if sufres:
        logger.info('key of ip matches ips keyword')


def get_ip_lists(ipdirs, ip_ports):
    if ip_ports == '':
        logger.error('ip information is null')
    else:  # 10.1.72.6~10:22,10.1.72.13:22
        ip_lists = ip_ports.split(',')  # ip列表是有逗号进行区分
        for i in range(len(ip_lists)):
            res = re.match(r'(.*\d+\.)+(\d+)~(\d+):(\d+)', ip_lists[i])
            if res:
                for inc in range(int(res.group(2)), int(res.group(3)) + 1):
                    mid_ip = res.group(1) + str(inc)
                    ipdirs[mid_ip] = res.group(4)
            else:
                ip, port = ip_lists[i].split(':')
                ipdirs[ip] = port
    logger.info(f'information of ip is dict {ipdirs}')
    return ipdirs
# ipdirs = {}
# ipdirs = get_ip_lists(ipdirs,ipandports='10.1.72.6~10:22,10.1.72.13:22')

cfg_mapping = {}
def get_config_dict(file):
    utils.config.read(file)
    content = utils.config['default']
    ipdirs = {}
    for key in content:
        if re.match('.*ips\Z', key):
           cfg_mapping[key] = get_ip_lists(ipdirs, content[key])
        else:
            cfg_mapping[key] = content[key]

#
# get_config_dict(utils.mysql_cfg_path)
# logger.info(cfg_mapping)

def test_compile():
    str = '10.1.72.6~8:22,10.1.72.10:22'
    res = re.match(r'(\d+\.\d+\.\d+\.\d+(~\d+)?:\d+,?)+','str')
    if not res :
        logger.info('errr')
# test_compile()


dictcon = {}


def test_clear_dict():
    dictcon['1'] = 2
test_clear_dict()
print(dictcon)
dictcon.clear()
print(dictcon)
