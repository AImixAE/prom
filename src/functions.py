#!python3
import io
import os
import shutil as sl
import sys
import re

import json

import click as c
from rich import print

fdir = os.path.dirname(__file__)  # 当前文件所在文件夹
root = os.getcwd()  # 当前路径
platform = sys.platform  # 系统
assets_path = os.getenv("PROM_ASSETS_PATH") or f"{fdir}/../assets"


name = "ProM"
version = {"group": "Code", "tag": "Dev", "ver": [0, 0, 2], "dev": "Preview"}


supported_language = os.listdir(f"{assets_path}/repo")


def hidecmd(cmd: str):
    match platform:
        case "linux":
            cmd = f"{cmd} &> /dev/null"
        case "windows":
            # 实验性
            # 没有平台测试
            # 且可能随时出现错误
            cmd = f"{cmd} | Out-Null || {cmd} >nul"

    return os.system(cmd)


def hiderun(cmd: str):
    # 定义 IO
    hideio = io.StringIO()
    originalout = sys.__stdout__

    # 切换 IO
    sys.__stdout__ = hideio

    # 执行并且获取结果
    result = eval(cmd, globals=globals(), locals=locals())

    # 切换到原本的 IO
    sys.__stdout__ = originalout

    return (result, hideio.getvalue())


def recursive_get(context: dict, *lst):
    if not (context and lst):
        return

    pre_context = context

    for i in lst:
        if i not in pre_context:
            return

        pre_context = pre_context[i]

    return pre_context


def secure_queries(context: dict, *lst, null=None):
    res = []

    for i in lst:
        if i in context:
            res.append(context[i])
        else:
            res.append(null)

    return res


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


@c.group()
def cli():
    pass


# 我认为最终它会变得越来越彭大 10/26/2024 --AImixAE
# 我丢怎么还TM的少了??! 12/28/2024 --AImixAE
@c.command(help="Initialize Project")
@c.argument("path")
@c.option("-r", "--readme", is_flag=True, help="Add README.md to your project")
@c.option(
    "-l",
    "--lang",
    "--language",
    "language",
    default="None",
    help="Define the project language",
)
@c.option(
    "-p",
    "--project-name",
    "name",
    default="",
    help="Define the project name",
)
def init(
    path: str,
    readme: bool,
    language: str,
    name: str,
):
    friendly_path = path.split("/")[-1]

    if os.path.isdir(path):
        print(
            "[yellow]Warning:[/yellow]",
            "Folder already exist!",
        )
        return

    print(f"Create {path}")

    mkdir(f"{root}/{path}")
    mkdir(f"{root}/{path}/src")
    os.chdir(f"{root}/{path}")

    if not name:
        name = friendly_path

    if readme:
        writefile(f"{root}/{path}/README.md", f"# {name}")

    if language in supported_language:
        copydir(f"{assets_path}/repo/{language}", f"{root}/{path}")

        repfile(f"{root}/{path}/prom.json", "%name%", name)
    else:
        print(
            "[yellow]Warning:[/yellow]",
            "Invalid or unsupported language,",
            "skipping...",
        )

    print("Create [green]Ok![/green]")


@c.command(help="Run Project")
@c.argument("target", default="main")
def run(target: str):
    if not os.path.isfile(f"{root}/prom.json"):
        print(
            "[yellow]Error:[/yellow]",
            "prom.json does not exist!",
        )
        return

    with open(f"{root}/prom.json", mode="rb") as f:
        t = json.load(f)

    command_list: list[dict] = recursive_get(t, target, "run") or []

    for commands in command_list:
        command, args = secure_queries(commands, "command", "argv")

    argv = ""

    for arg in args:
        argv += str(arg)

    os.system(f"{command} {argv}")


cli.add_command(init)
cli.add_command(run)
