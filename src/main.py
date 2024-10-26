#!python3
import click as c
from rich import print
import sys
import os
import io

root = os.getcwd()    # 当前路径
pf   = sys.platform   # 系统

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

def mkdir(p):
    print(f"Creating Folder '{p}' ...", end="")
    
    os.makedirs(p, exist_ok=True)
    
    print("OK")

def writefile(filename: str, basepath: str="", context: str=""):
    filename = filename.strip("/")
    basepath = basepath.strip("/")

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

@c.command(help="Initialize Project")
@c.argument("path")
@c.option("-g", "--git", is_flag=True, help="Initialize git repository")
@c.option("-r", "--readme", is_flag=True, help="Add README.md to your project")
@c.option("-p", "--project-name", "name", default="ProjectName", help="Define the project name")
def init(path: str, git: bool, readme: bool, name):
    path = path.strip("/")
    
    mkdir(path)
    os.chdir(f"{root}/{path}")
    mkdir("src")
    mkdir("doc")

    if git:
        gitinit(path)

    if readme:
        writefile("README.md", f"{root}/{path}", f"# {name}")


cli.add_command(init)

if __name__ == "__main__":
    cli()
