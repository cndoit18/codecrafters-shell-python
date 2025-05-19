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

        command = parse_line(input())
        match command:
            case cmd, *args if cmd in builtin:
                builtin[cmd](*args)
            case cmd, *args if cmd in path:
                fullpath = path[cmd].split(os.pathsep)[0]
                subprocess.run([cmd, *args], executable=fullpath)
            case cmd, *args if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
                subprocess.run([cmd, *args])
            case cmd, *_:
                print(f"{cmd}: command not found")


def parse_line(command: str) -> list[str]:
    command = command.replace("~", os.path.expanduser("~"))
    cmds = []
    previous_is_string = False
    while command:
        c = ""
        match command[0]:
            case '"' | "'":
                sign = command[0]
                command = command[1:]
                while command and command[0] != sign:
                    c += command[0]
                    command = command[1:]
                if command:
                    command = command[1:]
                if previous_is_string:
                    cmds[-1] += c
                    continue
                previous_is_string = True
            case " ":
                command = command[1:]
                previous_is_string = False
                continue
            case _:
                while command and command[0] != " ":
                    c += command[0]
                    command = command[1:]
                previous_is_string = False
        cmds.append(c)
    return cmds


if __name__ == "__main__":
    main()
