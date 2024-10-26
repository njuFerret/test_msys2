#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sys_info.py
@Time    :   2024/10/23 08:20:30
@Author  :   Ferret@NJTech 
@Version :   1.0
@Contact :   Ferret@NJTech
@License :   (C)Copyright 2024, Ferret@NJTech
@Desc    :   补充描述 
'''

from datetime import datetime
import os
import logging
import subprocess
import pathlib
import platform
import shutil
import string

START = datetime.now()
thisScript = pathlib.Path(__file__)
logLevel = logging.INFO
logFile = thisScript.with_suffix('.log')

# fmt:off
# Basic logging configuration
logging.basicConfig(
    level=logLevel,
    format='%(message)s' if logLevel == logging.INFO else '%(asctime)s %(filename)s(%(lineno)04d) [%(levelname)-8s]: %(message)s',
    handlers=[logging.FileHandler(logFile, mode='w', encoding='utf-8'), logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S'
)
# fmt:on


def runCommand(cmd, Env=None, workingPath=None, showMessage=True):
    '''
    执行shell命令, windows平台下为dos命令
    '''
    log_method = logging.info if showMessage else logging.debug
    # fmt: off
    process = subprocess.Popen(cmd, shell=True, env=Env, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=workingPath)
    # fmt: on
    rsts = []
    # 即时输出
    while True:
        rst = process.stdout.readline()
        try:
            rst = rst.decode("utf8")
        except:
            rst = rst.decode("GBK")
        rsts.append(rst)
        rst = rst.strip()
        if rst == '' and process.poll() is not None:
            break
        if rst:
            log_method(rst)
        process.poll()
    return ''.join(rsts).strip()


def sys_info(env=os.environ):

    def get_space(volumns):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        for idx, unit in enumerate(units):
            if (volumns >> 10 * (idx)) < (2 << 10):
                return "{} {}".format(volumns >> 10 * (idx), unit)

    # logging = logging
    logging.info('Os Info: ')
    machine = "x86_64" if '64' in platform.machine() else 'x86'
    msg = "  >>    OS: {}_{}_{} ver.{}, \t Computer Name:  {}".format(
        platform.system(), platform.release(), machine, platform.version(), platform.node()
    )
    logging.info(msg)
    msg = "  >>  Processor: {}, ".format(platform.processor())
    logging.info(msg)
    msg = "  >>  Processor cores: {}, ".format(os.cpu_count())
    logging.info(msg)
    msg = "  >>     AppData: {}, ".format(env.get('LOCALAPPDATA'))
    logging.info(msg)
    msg = "  >>    script info: {}".format(os.path.abspath(__file__))
    logging.info(msg)
    msg = "  >>        Path:\n"
    for p in sorted([d for d in env.get('PATH').split(';') if d]):
        msg += f"  >>              {p}\n"
    logging.info(msg)
    logging.info("  >>    Disks: ")
    for disk in list("CDE"):  # list(string.ascii_uppercase):
        try:
            _total, _used, _free = shutil.disk_usage("{}:/".format(disk))
            msg = "  >> \tDisk {}: Capacity({})/Used({})/Free({})".format(
                disk, get_space(_total), get_space(_used), get_space(_free)
            )
            logging.info(msg)
        except Exception as e:
            logging.debug(e)
    logging.info("")

    logging.debug('All Envs: ')
    for k, v in env.items():
        if k.upper() == 'PATH':
            continue
        logging.info('\t {}: {}'.format(k, v))


# def modify_msys_cmd_file():
#     logging.info('------------- content of msys2.CMD  ------------------')
#     msys_cmd_file = r'D:\a\_temp\setup-msys2\msys2.CMD'
#     msys_cmd_file = pathlib.Path(msys_cmd_file)
#     if not msys_cmd_file.exists():
#         logging.info(f' >  {msys_cmd_file} not exists')
#         return

#     # content = msys_cmd_file.open('r', encoding='utf-8').read()
#     # logging.info(content + '\n')
#     # content = content.replace('minimal', "inherit")
#     # logging.info(content + '\n')

#     # 修改配置文件，使MSYS2使用系统环境变量
#     content = msys_cmd_file.open('r', encoding='utf-8').read().replace('minimal', "inherit")
#     with msys_cmd_file.open('w', encoding='utf-8') as f:
#         f.write(content)


def list_foler(folder, show='folder'):
    if show not in ['all', 'folder', 'file']:
        show = 'folder'
    logging.info(f'-------------  folder in {folder} ------------------')
    folder = pathlib.Path(f'{folder}')
    if not folder.exists():
        logging.info(f' >  {folder} not exists')
        return
    logging.info(f' >  {folder}:')
    if show == 'all':
        what = [d for d in folder.iterdir()]
    elif show == 'folder':
        what = [d for d in folder.iterdir() if d.is_dir()]
    else:
        what = [d for d in folder.iterdir() if d.is_file()]

    for d in what:
        logging.info(f'\t\t{d}')

    logging.info("\n")


def main():

    sys_info()
    # show_msys_cmd_file()
    # list_foler(r'C:\Program Files', show='folder')
    # list_foler(r'C:\Program Files (x86)', show='folder')
    # list_foler(r'C:\hostedtoolcache\windows', show='folder')
    list_foler(r'C:\Program Files\7-zip', show='all')
    # list_foler(r'D:\a\_temp\msys64', show='all')


if __name__ == '__main__':
    # fmt: off
    logging.info('脚本 %s 开始运行, 时间: %s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    logging.info('脚本 %s 运行完成, 时间: %s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # fmt: on
