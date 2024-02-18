import os
import json
import utilities


def main():
    data_path = utilities.get_data_path(tree_level=2)
    messages = os.path.join(data_path, "messages.txt")
    file_btc = os.path.join(data_path, "btc-usd.txt")

    with open(messages, "r") as file:
        file.readline()
        lines = [line for line in file.readlines()]

    print(lines)
        
            # lines = [json.loads(line.decode('utf-8')) for line in file.readlines()]
            # f_btc.write(b"Hello world")

if __name__ == "__main__":
    main()
