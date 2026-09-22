import sys
import os
import shutil
import subprocess


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            cmd = command[5:]

            if cmd in ["type", "echo", "exit"]:
                print(f"{command[5:]} is a shell builtin")

            elif path := shutil.which(cmd):
                print(f"{cmd} is {path}")
            else:
                if shutil.which(cmd):
                    subprocess.run([f"{cmd}"], check=False)

                # print(f"{cmd}: not found")
        else:
            print(f"{command}: not found")


if __name__ == "__main__":
    main()
