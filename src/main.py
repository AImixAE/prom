#!python3
import io
import os
import shutil as sl
import sys
import time

import click as c
from rich import print

root = os.getcwd()  # 当前路径
pf = sys.platform  # 系统
assets_path = os.getenv("PROM_ASSETS_PATH") or "./assets"


app_name = "ProM"
version = {"group": "Code", "tag": "Dev", "ver": [0, 0, 1], "dev": "Preview"}


supported_language = ["python", "python3", "None"]


def hidecmd(cmd: str):
    match pf:
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


def mkdir(p: str):
    friendly_p = p.split("/")[-1]

    print(f"Creating Folder '{friendly_p}' ...", end="")

    os.makedirs(p, exist_ok=True)

    print("OK")


def writefile(filename: str, context: str = ""):
    friendly_filename = filename.split("/")[-1]

    print(f"Writing to '{friendly_filename}' ...", end="")

    with open(filename, mode="w+") as f:
        f.write(context)

    print("OK")


def repfile(filename: str, old: str = "", new: str = ""):
    friendly_filename = filename.split("/")[-1]

    print(f"Replacing to '{friendly_filename}' ...", end="")

    with open(filename, mode="r") as f:
        o = str(f.read()).replace(old, new)

    with open(filename, mode="w+") as f:
        f.write(o)

    print("OK")


def copydir(src: str, target: str):
    friendly_src = src.split("/")[-1]
    friendly_target = target.split("/")[-1]

    print(f"Copying dir '{friendly_src}' to '{friendly_target}' ...", end="")

    sl.copytree(
        src, target, dirs_exist_ok=True
    )

    print("OK")


def gitinit(p):
    print("Initing [blue]Git[/blue] [green]Repo[/green] ...", end="")

    os.chdir(root + "/" + p)
    hidecmd("git init -b main")

    print("OK")


@c.group()
def cli():
    pass


# 我认为最终它会变得越来越彭大 10/26/2024
@c.command(help="Initialize Project")
@c.argument("path")
@c.option("-g", "--git", is_flag=True, help="Initialize git repository")
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
    git: bool,
    readme: bool,
    language: str,
    name: str,
):
    friendly_path = path.split("/")[-1]

    if os.path.isdir(path):
        print("[yellow]Warning: [/yellow] Folder already exist!")
        control = input("Continue? [y/N/d]")

        match control:
            case "y" | "Y":
                pass
            case "n" | "N" | "":
                print("bye")
                return
            case "d" | "D":
                print("Folder will be deleted in 2 seconds ...", end="")
                time.sleep(2)
                print("Deleting ...", end="")
                sl.rmtree(path)
                print("OK")
            case _:
                print("Is not a valid input!")
                return

    mkdir(f"{root}/{path}")
    mkdir(f"{root}/{path}/src")
    mkdir(f"{root}/{path}/src")
    os.chdir(f"{root}/{path}")

    if not name:
        name = friendly_path

    if git:
        gitinit(path)

    if readme:
        writefile(f"{root}/{path}/README.md", f"# {name}")

    if language in supported_language:
        copydir(f"{assets_path}/data/{language}", f"{root}/{path}")

        repfile(f"{root}/{path}/prom.toml", "%name%", name)
    else:
        print(
            "[yellow]Warning: [/yellow]" + "Invalid or unsupported language,",
            "skipping...",
        )


cli.add_command(init)

if __name__ == "__main__":
    ver = ""
    verlst = version["ver"]
    verlen = len(verlst)

    for i in range(verlen):
        ver += str(verlst[i])
        if i != verlen - 1:
            ver += "."

    print(
        f"[blue]{app_name}[/blue]",
        f"[yellow]{version['group']} {version['tag']}[/yellow]",
        f"[cyan]v{ver} [bold]{version['dev']}[/bold][/cyan]",
    )

    cli()
