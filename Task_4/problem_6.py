import platform
import datetime

def log_system_info(filename="sys_log.txt"):
    os_type = platform.system()
    timestamp = datetime.datetime.now()

    with open(filename, "a") as file:
        file.write(f"OS Type: {os_type} | Time: {timestamp}\n")


def main():
    log_system_info()

if __name__ == "__main__":
    main()