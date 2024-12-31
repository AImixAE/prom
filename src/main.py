#!python3
from fire import Fire as f
from rich import print

import sys
import os
import tomli

import functions as func
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
        self,
        path: str,
        readme: bool = False,
        language: str = "None",
        name: str = "",
    ):
        "Initialize Project"
        friendly_path = path.split("/")[-1]

        if os.path.isdir(path):
            func.err(
                FileExistsError(f"{friendly_path} already exists", "Try a new folder")
            )
            return 1

        print(f"Create {path}")

        func.mkdir(f"{d.root}/{path}")
        func.mkdir(f"{d.root}/{path}/src")
        os.chdir(f"{d.root}/{path}")

        if not name:
            name = friendly_path

        if readme:
            func.writefile(f"{d.root}/{path}/README.md", f"# {name}")

        if language in d.supported_language:
            func.copydir(f"{d.assets_path}/repo/{language}", f"{d.root}/{path}")

            func.repfile(f"{d.root}/{path}/prom.toml", "%name%", name)
        else:
            func.warn(UserWarning("Invalid or unsupported language,", "skipping"))

        print("Create [green]Ok![/green]")

    def run(self):
        "Run the project"
        if not os.path.isfile(f"{d.root}/prom.json"):
            func.err(FileNotFoundError("prom.json does not exist!"))
            return 1

        with open(f"{d.root}/prom.toml", mode="rb") as f:
            t = tomli.load(f)


if __name__ == "__main__":
    app = ProM()
    sys.exit(f(app))
