#!python3
from fire import Fire as f
from rich import print

import sys
import os

from functions import *
import data as d


class ProM:
    def __init__(self):
        print(
            f"[blue]{d.name}[/blue]",
            f"[yellow]{d.version['group']} {d.version['tag']}[/yellow]",
            f"[cyan]v{d.ver} [bold]{d.version['dev']}[/bold][/cyan]",
        )

        if len(sys.argv) > 1:
            print()

    def init(
        path: str,
        readme: bool = False,
        language: str = "None",
        name: str = "",
    ):
        "Initialize Project"
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

    def run(target: str = "main"):
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


if __name__ == "__main__":
    app = ProM()
    f(app)
