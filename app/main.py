import sys


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()
        match command.split():
            case "exit", *code:
                sys.exit(int(code[0]) if len(code) > 0 else 0)
            case "echo", *args:
                print(" ".join(args))
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
