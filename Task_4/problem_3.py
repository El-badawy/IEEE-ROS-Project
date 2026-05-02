def write_log(message, filename="log.txt"):
    with open(filename, "a") as file:
        file.write(message + "\n")


def read_logs(filename="log.txt"):
    try:
        with open(filename, "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("Log file not found.")


write_log("System started")
write_log("User logged in")

read_logs()