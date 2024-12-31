#!python3
import os
import sys
import shutil as sl
import re

from rich import print
import data as d


def warn(w: Exception):
    args = w.args

    print(f"[yellow]Warning:[/yellow] {args[0]}")

    for i in args[1:]:
        print(i)

    print(f"({w.__class__})")


def err(e: Exception):
    args = e.args
    print(f"[red]Error:[/red] {args[0]}")

    for i in args[1:]:
        print(i)

    print(f"[dim]({e.__class__})[/dim]")


def hidecmd(cmd: str):
    match d.platform:
        case "linux":
            cmd = f"{cmd} &> /dev/null"
        case "windows":
            # 实验性
            # 没有平台测试
            # 且可能随时出现错误
            cmd = f"{cmd} | Out-Null || {cmd} >nul"

    return os.system(cmd)


def get_toml_value(context: dict, key):
    pass


def mkdir(p: str):
    friendly_p = p.split("/")[-1]

    print(f"  [green][+][/green] {friendly_p}")

    os.makedirs(p, exist_ok=True)


def writefile(filename: str, context: str = ""):
    friendly_filename = filename.split("/")[-1]

    print(f"  [green][+][/green] {friendly_filename}")

    with open(filename, mode="w+") as f:
        f.write(context)


def repfile(filename: str, old: str = "", new: str = ""):
    friendly_filename = filename.split("/")[-1]

    print(f"  [green][R][/green] {friendly_filename}")

    with open(filename, mode="r") as f:
        o = re.sub(old, new, str(f.read()))

    with open(filename, mode="w+") as f:
        f.write(o)


def copydir(src: str, target: str):
    friendly_src = src.split("/")[-1]
    friendly_target = target.split("/")[-1]

    print(f"  [green][C][/green] {friendly_src} -> {friendly_target}")

    sl.copytree(src, target, dirs_exist_ok=True)


def checkfile(path: str):
    return os.path.exists(path)
