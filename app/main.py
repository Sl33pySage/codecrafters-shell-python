import subprocess, shutil, os, sys


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        if command == "exit":
            break

        elif command.startswith("cd "):
            try:
                os.chdir(command[3:])
            except:
                print(f"cd: {command[3:]}: No such file or directory")

        elif command == "pwd":
            print(os.getcwd())

        elif command.startswith("echo "):
            print(command[5:])

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
