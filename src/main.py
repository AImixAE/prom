import click as c
from rich import print
import sys
import os

root = os.getcwd()
pf = sys.platform

def hiderun(cmd: str):
    if pf == "linux":
        cmd = f"{cmd} &> /dev/null"

    return os.system(cmd)

def mkdir(p):
    print(f"Create Folder '{p}'")
    os.makedirs(p, exist_ok=True)

def gitinit(p):
    print("Init [blue]Git[/blue] [green]Repo[/green]")
    os.chdir(root + "/" + p)
    hiderun("git init -b main")


@c.group()
def cli():
    pass

@c.command(help="Initialize Project")
@c.argument("path")
@c.option("-g", "--git", is_flag=True)
def init(path: str, git: bool):
    path = path.strip("/")
    mkdir(path)
    os.chdir(root + "/" + path)
    mkdir("src")
    mkdir("doc")

    if git:
        gitinit(path)


cli.add_command(init)

if __name__ == "__main__":
    cli()
