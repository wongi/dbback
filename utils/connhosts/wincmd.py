# -*- coding: utf-8 -*-
from  utils import connhosts
import utils

logger = utils.get_logger()


def scripts_command(script_path, args):  # 脚本执行命令
    if args:
        cmd = f'{script_path} {args}'
        return cmd
    else:
        logger.error('args is null')
        raise ValueError


def exec_cmd(conn, cmd):  # 执行命令
    try:
        res = conn.run_cmd(cmd)
        results = res.std_out.decode('utf-8')
        return results
    except ConnectionAbortedError as e:
        logger.error(f'连接终止 {e}')
        raise ConnectionError


@utils.timer
def exec_scp(ftpcon, mode, target, dest):
    if mode.value == connhosts.Param.W.value:  # 上传
        pass
    if mode.value == connhosts.Param.R.value:  # 下载 E:\pscp.exe file root@192.168.1.147:/tmp/
        pass
