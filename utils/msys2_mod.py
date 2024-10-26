import pathlib

# import shutil
import winreg
import sys

root = pathlib.Path(__file__).parent

qt_ver = sys.argv[1]
pathes = sys.argv[2:]


def add_path_env(content, argvs):
    pth = []
    pth.append(r'C:\Windows')
    pth.append(r'C:\Windows\System32')
    for path in argvs:
        pth.append(path)

    pth = [p for p in pth if p.strip()]
    c = f'set PATH= {";".join(pth)}'
    old = content.splitlines()
    new = old[:-1] + [c] + old[-1:]
    return "\n".join(new)


def add_path_qt(content, qp_version):
    old = content.splitlines()
    new = old[:-1] + [f'set QT_ROOT=/D/Dev/Qt/{qp_version}'] + old[-1:]
    return "\n".join(new)


def modify_msys_cmd_file(msys_cmd_file=r'D:\a\_temp\setup-msys2\msys2.CMD'):
    msys_cmd_file = pathlib.Path(msys_cmd_file)
    if not msys_cmd_file.exists():
        print(f' >  {msys_cmd_file} not exists')
        return

    # 修改配置文件，使MSYS2使用系统环境变量
    content = msys_cmd_file.open('r', encoding='utf-8').read().replace('minimal', "inherit").strip()

    content = add_path_env(content, pathes)
    content = add_path_qt(content, qt_ver)

    with msys_cmd_file.open('w', encoding='utf-8') as f:
        f.write(content)
    print(content)


modify_msys_cmd_file()
