import os
import shutil
import sys
import shlex
import subprocess


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if not command:
            continue

        parts = shlex.split(command)
        program = parts[0]

        if command == "exit":
            break

        if command == "pwd":
            print(os.getcwd())
            continue

        if program == "echo":
            print(" ".join(parts[1:]))
            continue

        if program == "type":
            target = parts[1]
            if target in {"exit", "echo", "type", "pwd", "cd"}:
                print(f"{target} is a shell builtin")
            else:
                executable_path = shutil.which(target)
                if executable_path:
                    print(f"{target} is {executable_path}")
                else:
                    print(f"{target}: not found")
            continue

        if command == "cd" or command.startswith("cd "):
            target = command[2:].strip() or "~"
            try:
                os.chdir(os.path.expanduser(target))
            except (FileNotFoundError, NotADirectoryError, PermissionError):
                print(f"cd: {target}: No such file or directory")
            continue

        if shutil.which(program):
            subprocess.run(parts)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
