from email.mime import base
import os

ignore = [
    ".git",
    ".gitattributes",
    ".gitignore",
    "autopytoexeConfig.json",
    "bugs.txt",
    "builds",
    "saves",
    "__pycache__",
    "entity/__pycache__",
    "entity/view/__pycache__",
    "entity/model/__pycache__",
    "skyscript/__pycache__",
    "README.md",
    "Skylands WFA.lnk",
    "generate_filepaths.py",
    "launcher.py",
    "filepaths",
]

filepaths = []

def list_folder(base_path):
    global filepaths

    files = os.listdir(base_path if base_path != "" else None)

    for file in files:
        filepath = "/".join((base_path, file)) if base_path != "" else file
        if not filepath in ignore:
            print(filepath, os.path.isdir(filepath))
            if os.path.isdir(filepath):
                list_folder(filepath)
            else:
                filepaths.append(filepath)

list_folder("")

f = open("filepaths", "w")
f.write("\n".join(filepaths))
f.close()