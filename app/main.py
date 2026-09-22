import subprocess, shutil, os, sys


def builtin_commands(c):
    return c in {"echo", "exit", "type"}


def execute_commands(c):
    for d in os.get_exec_path():
        if os.access(fullpath := os.path.join(d, c), os.X_OK):
            return fullpath


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().strip()

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else ""

        if builtin_commands(cmd):
            if cmd == "exit":
                break
        elif cmd == "echo":
            print(f"{' '.join(args)}")
        elif cmd == "type":
            if builtin_commands(args[0]):
                print(f"{args[0]} is a shell builtin")
            elif fullpath := execute_commands(args[0]):
                print(f"{args[0]} is {fullpath}")
            else:
                print(f"{args[0]}: not found")

        elif execute_commands(cmd):
            subprocess.run(parts)
        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
