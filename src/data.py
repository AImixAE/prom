import os
import sys

name = "ProM"
version = {"group": "Code", "tag": "Dev", "ver": [0, 0, 2], "dev": "Preview"}

ver = ""
verlst = version["ver"]
verlen = len(verlst)

for i in range(verlen):
    ver += str(verlst[i])
    if i != verlen - 1:
        ver += "."

fdir = os.path.dirname(__file__)  # 当前文件所在文件夹
root = os.getcwd()  # 当前路径
platform = sys.platform  # 系统
assets_path = os.getenv("PROM_ASSETS_PATH") or f"{fdir}/../assets"

supported_language = os.listdir(f"{assets_path}/repo")
