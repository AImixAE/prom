#!python3
import core as c
from rich import print

if __name__ == "__main__":
    ver = ""
    verlst = c.version["ver"]
    verlen = len(verlst)

    for i in range(verlen):
        ver += str(verlst[i])
        if i != verlen - 1:
            ver += "."

    print(
        f"[blue]{c.name}[/blue]",
        f"[yellow]{c.version['group']} {c.version['tag']}[/yellow]",
        f"[cyan]v{ver} [bold]{c.version['dev']}[/bold][/cyan]",
    )
    print()

    c.cli()
