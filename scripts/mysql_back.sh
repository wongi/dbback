#!/bin/bash

host_bak_file_dir_name='/root/mysql/backup/data'
host_bak_log_dir_name='/root/mysql/backup/logs'
time='date "+%Y%m%d"'
echo 'mysqlbackup  data success' > $host_bak_file_dir_name/full_mysql_${time}.mysql
echo 'mysqlbackup  log  success' > /root/mysql/backup/log/full_mysql_${time}.log