import os
import shutil
import shlex
import subprocess
import sys


def exit_command(_arguments):
    return False


def echo_command(arguments):
    print(arguments)
    return True


def type_command(arguments):
    if COMMANDS.get(arguments) is not None:
        print(f"{arguments} is a shell builtin")
    elif path := shutil.which(arguments):
        print(f"{arguments} is {path}")
    else:
        print(f"{arguments}: not found")
    return True


def cd_command(arguments):
    path = os.path.expanduser(arguments or "~")
    try:
        os.chdir(path)
    except OSError as error:
        print(f"cd: {arguments}: {error.strerror}")
    return True


COMMANDS = {
    "exit": exit_command,
    "echo": echo_command,
    "type": type_command,
    "pwd": lambda _: print(os.getcwd()) or True,
    "cd": cd_command,
}


def run_command(command):
    name, separator, arguments = command.partition(" ")
    handler = COMMANDS.get(name)

    if ">" in command or "1>" in command:
        os.system(command)
        return True
    if handler is not None:
        return handler(arguments if separator else "")

    executable = shutil.which(name)
    if executable is None:
        print(f"{name}: command not found")
        return True

    command_arguments = shlex.split(command)
    subprocess.run(command_arguments, executable=executable, check=False)
    return True


def main():
    while True:
        sys.stdout.write("$ ")
        command = input("")
        if not run_command(command):
            break


if __name__ == "__main__":
    main()
