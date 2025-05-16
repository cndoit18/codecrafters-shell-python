import sys

builtin = {
    "exit": lambda *code: sys.exit(int(code[0]) if len(code) > 0 else 0),
    "echo": lambda *args: print(" ".join(args)),
}


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()
        match command.split():
            case "exit", *code:
                builtin["exit"](*code)
            case "echo", *args:
                builtin["echo"](*args)
            case "type", cmd:
                if cmd in builtin or cmd == "type":
                    print(f"{cmd} is a shell builtin")
                else:
                    print(f"{cmd}: not found")
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
