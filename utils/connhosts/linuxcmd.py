# -*- coding: utf-8 -*-
from utils import connhosts
import utils
import os.path
import tarfile
logger = utils.get_logger()


def scripts_command(script_path, args):  # 脚本命令入参
    if args:
        cmd = f'{script_path} {args}'
        return cmd
    else:
        logger.error('args is null')
        raise ValueError


def exec_cmd(conn, cmd):  # 执行命令
    try:
        stdin, stdout, stderr = conn.exec_command(cmd)
        results = stdout.read().decode('utf-8')
        return results
    except ConnectionAbortedError as e:
        logger.error(f'连接终止 {e}')
        raise ConnectionError


@utils.timer
def exec_scp(ftpcon, mode, target, dest):
    if mode.value == connhosts.Param.W.value:  # 上传
        ftpcon.put(target, dest)
    if mode.value == connhosts.Param.R.value:  # 下载
        ftpcon.get(target, dest)


def tar_file(file, name=''):  # 压缩文件
    base = os.path.dirname(file)
    print(base)
    if os.path.isdir(file):  # 提取父类目录 /Users/threeboys33/tools/backup_check
        name = os.path.basename(file) + '.tar.gz'  # backup_check.tar.gz
        tar = tarfile.open(base + os.sep + name, 'w:gz')  # /Users/threeboys33/tools/backup.tar.gz
        for i in os.listdir(file):
            tar.add(file + os.sep + i)
        return base + os.sep + name

    elif os.path.isfile(file):
        if tarfile.is_tarfile(file):
            return file
        else:
            tar = tarfile.open(name, 'w:gz')
            tar.add(file)
            return base + os.sep + name