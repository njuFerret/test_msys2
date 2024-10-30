#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   copy_examples_src-for-Qt6.py
@Time    :   2023/08/31 14:57:49
@Author  :   Ferret@NJTech 
@Version :   1.0
@Contact :   Ferret@NJTech
@License :   (C)Copyright 2023, Ferret@NJTech
@Desc    :   Qt 6.x编译后examples目录下仅有exe文件, 而无源文件 
             本脚本根据生成的exe文件, 复制相应文件夹至qt/examples目录下             
'''

from datetime import datetime
import logging
import shutil
import pathlib


START = datetime.now()
logger = None
thisScript = pathlib.Path(__file__)


def setupLogger(logLevel=logging.DEBUG):
    global logger
    # logFileName = thisScript.with_name(thisScript.stem + format(START, '_%Y%m%d-%H%M%S.log'))
    logFileName = thisScript.with_suffix('.log')
    logger = logging.getLogger(__name__)
    logger.setLevel(logLevel)
    fh = logging.FileHandler(logFileName, 'w', 'utf-8')
    ch = logging.StreamHandler()
    if logLevel == logging.DEBUG:
        fmtStr = '%(filename)s(%(lineno)04d) [%(levelname)-8s]: %(message)s'
    else:
        fmtStr = '%(message)s'
    logFmt = logging.Formatter(fmt=fmtStr, datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(logFmt)
    ch.setFormatter(logFmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger



def remove_unused_lang_pack(qt_install_dir):
    #base_dir = r'D:\Dev\Qt\6.5.3'
    base_dir = pathlib.Path(qt_install_dir)
    qt_dir = base_dir / 'qt'
    qtc_dir = base_dir / 'qtcreator'

    qt_trans_dir = qt_dir / 'translations'
    qtc_trans_dir = qtc_dir / 'share/qtcreator/translations'

    translations = [t for t in qt_trans_dir.glob('**/*.qm') if 'zh_CN' not in t.name]
    translations.extend([t for t in qtc_trans_dir.glob('**/*.qm') if 'zh_CN' not in t.name])
    #print(translations)

    for translation in translations:
        logger.info(f'删除无用翻译文件：{translation}')
        translation.unlink()

def copy_examples_src(qt_base_dir, qt_src_dir):
    qt_src = pathlib.Path(qt_src_dir)
    qt_base_dir = pathlib.Path(qt_base_dir)
    examples_install_dir = qt_base_dir / 'qt/examples'
    fake_examples_dir = examples_install_dir.with_name('examples1')
    
    logger.info(f"[examples安装路径]: {examples_install_dir}")
    
    logger.info('搜索目录较慢，请耐心等待....')
    # 搜索所有以examples结尾的目录，不包括第三方库的目录
    base=[ p for p in qt_src.glob('**/examples')  if p.is_dir() and '3rdparty' not in str(p)]

    logger.info(f" - 找到 {len(base)} 个包含 'examples' 目录")

    # 找出所有已安装的目录
    installed =[d.name for d in examples_install_dir.glob('*') if d.is_dir()]
    logger.info(f" - 找到 {len(installed)} 个已安装的例程目录")

    # 有效目录，1.该目录在 base目录下
    valid_examples = [ p/d for p in base for d in installed if (p/d).exists()]
    logger.info(f" - 找到 {len(valid_examples)} 个有效例程目录")


    for src_dir in valid_examples:
        logger.info(f'copying {src_dir} to {examples_install_dir/src_dir.name}... '.replace(str(qt_src),'[qt_src]').replace(str(examples_install_dir),'[examples_install_dir]'))
        shutil.copytree(src_dir,examples_install_dir/src_dir.name,dirs_exist_ok=True)

    # 根据已编译的示例程序exe文件，复制代码文件
    for d in examples_install_dir.glob('**/*.exe'):
        src_dir = d.parent
        fake = fake_examples_dir / (d.relative_to(examples_install_dir).parent)
        # fake.mkdir(parents=True,exist_ok=True)
        logger.info(f'copy  {src_dir} to {fake}...')
        shutil.copytree(src=src_dir,dst=fake,dirs_exist_ok=True)

    # 漏掉的文件
    # [QT_SRC]\qtbase\examples\sql\connection.h    
    logger.info(f" -> 复制  {qt_src/'qtbase/examples/sql/connection.h'} 至 {fake_examples_dir/'sql/connection.h'} ...")
    shutil.copy(qt_src/'qtbase/examples/sql/connection.h',fake_examples_dir/'sql/connection.h')

    # 删除旧的examples目录
    shutil.rmtree(examples_install_dir,ignore_errors=True)
    # 将examples1目录重命名为examples
    fake_examples_dir.rename(examples_install_dir)    




def main():

    qt_ver = '6.5.3'

    qt_src = f'E:/bb/qt-everywhere-src-{qt_ver}'
    qt_base_dir = f'D:/Dev/Qt/{qt_ver}'
    

    logger.info(f"[qt_src]: {qt_src}")
    logger.info(f"[qt_base_dir]: {qt_base_dir}")
   
    logger.info(f"删除无用语言包....")
    remove_unused_lang_pack(qt_base_dir)

    logger.info(f"复制 examples 文件夹....")
    copy_examples_src(qt_base_dir, qt_src)
    


if __name__ == '__main__':
    setupLogger(logLevel=logging.INFO)
    logger.info('脚本 % s 开始运行, 时间：% s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    main()
    logger.info('脚本 %s 运行完成, 时间：%s ' %(thisScript.name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))



