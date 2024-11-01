#!python3
import io
import os
import sys

import click as c
from rich import print

root = os.getcwd()  # 当前路径
pf = sys.platform  # 系统


def hidecmd(cmd: str):
    if pf == "linux":
        cmd = f"{cmd} &> /dev/null"

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


def mkdir(p, basepath: str = ""):
    print(f"Creating Folder '{p}' ...", end="")

    os.makedirs(f"{basepath}/{p}", exist_ok=True)

    print("OK")


def writefile(filename: str, basepath: str = "", context: str = ""):
    print(f"Writing to '{filename}' ...", end="")

    with open(f"{basepath}/{filename}", mode="w+") as f:
        f.write(context)

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
@c.option("-m", "--makefile", is_flag=True, help="Add Makefile to your project")
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
    default="ProjectName",
    help="Define the project name",
)
def init(path: str, git: bool, readme: bool, makefile: bool, language: str, name: str):
    tomake: bool = False

    mkdir(path, root)
    mkdir("src", f"{root}/{path}")
    mkdir("doc", f"{root}/{path}")
    os.chdir(f"{root}/{path}")

    if git:
        gitinit(path)

    if readme:
        writefile("README.md", f"{root}/{path}", f"# {name}")

    match language:
        case "python" | "python3":
            writefile("main.py", f"{root}/{path}/src", "#!python3\n\nprint(\"Hello, World!\")")

        case "clang" | "c":
            tomake = True

        case "clang++" | "c++" | "cpp":
            tomake = True

        case "None":
            pass

        case _:
            print(
                "[yellow]Warning: [/yellow]" +
                "Invalid or unsupported language,",
                "skipping...",
            )

    # TODO
    if tomake and makefile:
        pass


cli.add_command(init)

if __name__ == "__main__":
    cli()
