name = "ProM"
version = {"group": "Code", "tag": "Dev", "ver": [0, 0, 2], "dev": "Preview"}

ver = ""
verlst = version["ver"]
verlen = len(verlst)

for i in range(verlen):
    ver += str(verlst[i])
    if i != verlen - 1:
        ver += "."
