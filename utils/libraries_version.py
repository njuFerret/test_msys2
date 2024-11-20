import pathlib

base_dir = pathlib.Path(__file__).parent
version_file = base_dir.parent / "libraries_version.txt"
version_folder = base_dir.parent.joinpath("versions")
version_folder.mkdir(exist_ok=True, parents=True)


runs = []
outputs = []
checks = []

for line in version_file.open("r", encoding='utf-8').readlines():
    if line.startswith("#") or line.strip() == "":
        continue
    # 移除行内注释
    line = line[: line.find('#')].strip() if '#' in line else line.strip()

    lib, version = line.split("=", 1)
    lib = lib.strip()
    version = version.strip()

    with version_folder.joinpath(f"{lib}").open("w", encoding='utf-8') as f:
        f.write(f'{version}')

    # 以下为创建versions_config任务中的各个输出变量
    if '_' in lib and 'link' in lib:
        tmpl = 'echo "{}=$(cat versions/{})" >> $GITHUB_OUTPUT'
        runs.append(tmpl.format(lib.replace('_', '-'), lib))
        output = lib.replace('_', '-')
    elif '_' in lib:
        tmpl = 'echo "{}=$(cat versions/{})" >> $GITHUB_OUTPUT'
        runs.append(tmpl.format(lib.replace('_', '-'), lib))
        output = lib.replace('_', '-')
    else:
        tmpl = 'echo "{}-version=$(cat versions/{})" >> $GITHUB_OUTPUT'
        runs.append(tmpl.format(lib, lib))
        output = f'{lib}-version'
    out_fmt = '{LIB}: ${{{{ steps.get-versions.outputs.{LIB} }}}}'
    outputs.append(out_fmt.format(LIB=output))
    check_fmt = 'echo "{LIB}=${{{{ needs.versions_config.outputs.{LIB} }}}}"'
    checks.append(check_fmt.format(LIB=output))


print('\noutputs: ')
for output in outputs:
    print(output)

print('\n\nrun: |')
for run in runs:
    print(run)

print('\n\nrun: | (in check)')
for check in checks:
    print(check)
