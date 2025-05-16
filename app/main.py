import sys
import os
import subprocess


def load_path():
    path = {}
    for dir in filter(os.path.isdir, os.getenv("PATH", "").split(os.pathsep)):
        for bin in filter(
            lambda b: os.access(os.path.join(dir, b), os.X_OK), os.listdir(dir)
        ):
            fullpath = os.path.join(dir, bin)
            path[bin] = (
                f"{path.get(bin)}{os.pathsep}{fullpath}" if bin in path else fullpath
            )
    return path


path = load_path()

builtin = {
    "exit": lambda *code: sys.exit(int(code[0]) if len(code) > 0 else 0),
    "echo": lambda *args: print(" ".join(args)),
    "type": lambda cmd: print(
        f"{cmd} is a shell builtin"
        if cmd in builtin
        else f"{cmd} is {path[cmd].split(os.pathsep)[0]}"
        if cmd in path
        else f"{cmd}: not found",
    ),
    "pwd": lambda *_: print(os.getcwd()),
    "cd": lambda path: os.chdir(path)
    if os.path.isdir(path)
    else print(f"cd: {path}: No such file or directory"),
}


def main():
    while True:
        sys.stdout.write("$ ")

        command = input().replace("~", os.path.expanduser("~"))
        match command.split():
            case cmd, *args if cmd in builtin:
                builtin[cmd](*args)
            case cmd, *args if cmd in path:
                fullpath = path[cmd].split(os.pathsep)[0]
                subprocess.run([cmd, *args], executable=fullpath)
            case cmd, *args if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
                subprocess.run([cmd, *args])
            case cmd, *_:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
