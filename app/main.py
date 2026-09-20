import sys
import os


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command[5:] in ["type", "echo", "exit"]:
            print(f"{command[5:]} is a shell builtin")
        else:
            os_path = os.get_exec_path()
            path_line = 0
            for path_line in os_path:
                # print(os.access(path_line, os.X_OK))
                if path_line.endswith(command[5:]) and os.access(path_line, os.X_OK):
                    print(f"{command[5:]} is {path_line}")
                    break
                print(f"{command.strip('type')}: not found")


if __name__ == "__main__":
    main()
