import os
import pathlib
import shlex
import shutil
import subprocess
import sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        parts = shlex.split(command)
        program = parts[0]

        if command == "exit":
            break

        elif command.startswith("cd "):
            if command[3:] == "~":
                os.chdir(pathlib.Path.home())
            else:
                try:
                    os.chdir(command[3:])
                except (FileNotFoundError, NotADirectoryError, PermissionError):
                    print(f"cd: {command[3:]}: No such file or directory")

        elif command == "pwd":
            print(os.getcwd())

        elif command.startswith("echo "):
            # print(command[5:])
            print(" ".join(parts[1:]))
            continue

        elif command.startswith("type"):
            cmd = command[5:]

            if cmd in ["echo", "type", "exit", "pwd", "cd"]:
                print(f"{cmd} is a shell builtin")

            elif path := shutil.which(cmd):
                print(f"{cmd} is {path}")

            else:
                print(f"{cmd}: not found")

        else:
            parts = command.split()

            if parts and shutil.which(parts[0]):
                subprocess.run(parts)
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
