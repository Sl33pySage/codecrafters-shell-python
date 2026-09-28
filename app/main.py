import sys
import os
import shlex
import subprocess

BUILT_INS = {
    "echo": lambda args: print(args),
    "pwd": lambda _: print(os.getcwd()),
    "type": lambda args: checkType(args),
    "cd": lambda args: cd_handler(args),
}


def cd_handler(args: str):
    target = os.path.expanduser(args)
    os.chdir(target) if os.path.isdir(target) else print(
        f"cd: {target}: No such file or directory"
    )


def checkType(args: str):
    if args in ["echo", "type", "exit", "pwd"]:
        print(f"{args} is a shell builtin")
    elif (res := isExecutableFile(args))[0]:
        print(f"{args} is {res[1]}")
    else:
        print(f"{args}: not found")


def isExecutableFile(file_input: str) -> tuple[bool, str]:
    res = False
    paths = os.getenv("PATH")

    if paths == None:
        return res

    directories_to_check: list[str] = paths.split(os.pathsep)

    file_path = None

    for directory_path in directories_to_check:
        if os.path.exists(directory_path):
            file_path: str = os.path.join(directory_path, file_input)
            if os.path.exists(file_path) and os.access(file_path, os.X_OK):
                res = True
                break

    return res, file_path


def main():
    while True:
        sys.stdout.write("$ ")
        command = shlex.split(input())

        redirect_at = None
        for i, token in enumerate(command):
            if token == ">" or token == "1>":
                redirect_at = i
                break

        if redirect_at is None:
            argv = command
            out_file = None
        else:
            argv = command[:redirect_at]
            out_file = command[redirect_at + 1]

        command_name = argv[0]
        command_args = argv[1:]

        stdout_file = open(out_file, "w") if out_file is not None else None
        old_stdout = sys.stdout
        try:
            if command_name == "exit":
                break
            elif command_name in BUILT_INS:
                if stdout_file is not None:
                    sys.stdout = stdout_file
                BUILT_INS[command_name](" ".join(command_args))
            elif (res := isExecutableFile(command_name))[0]:
                subprocess.run(argv, stdout=stdout_file)
            else:
                print(f"{command_name}: command not found")
        finally:
            sys.stdout = old_stdout
            if stdout_file is not None:
                stdout_file.close()


if __name__ == "__main__":
    main()

    # command = input()

    # if not command:
    #    continue

    # parts = shlex.split(command)
    # program = parts[0]

    # if ">" in parts:
    # with open(parts[1], "r") as file:
    #   content = file.read()
    #    with open(parts[3], "w") as file2:
    #        file2.write(content)
#
#        if command == "exit":
#            break
#
#        if command == "pwd":
#            print(os.getcwd())
#            continue
#
#        if program == "echo":
#            print(" ".join(parts[1:]))
#            continue
#
#        if program == "type":
#            target = parts[1]
#            if target in {"exit", "echo", "type", "pwd", "cd"}:
#                print(f"{target} is a shell builtin")
#            else:
#                executable_path = shutil.which(target)
#                if executable_path:
#                    print(f"{target} is {executable_path}")
#                else:
#                    print(f"{target}: not found")
#            continue
#
#        if command == "cd" or command.startswith("cd "):
#            target = command[2:].strip() or "~"
#            try:
#                os.chdir(os.path.expanduser(target))
#            except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
#                print(f"cd: {target}: No such file or directory")
#            continue
#
#    if shutil.which(program):
#     subprocess.run(parts)
# else:
#   print(f"{command}: command not found")
