from src.cmd import parse_input
from src.table import group, get_keys, printing


data = parse_input()

def main(data):
    for file in data:
        key = get_keys(file[0])
        employees = group(file)
        printing(employees, key)


if __name__ == "__main__":
    main(data)