from src.cmd import parse_input
from src.view import group, get_keys, payout_report


data = parse_input()

def main(data: list):
    for file in data:
        headers = get_keys(file[0])
        employees = group(file)
        payout_report(employees, headers['rate'])


if __name__ == "__main__":
    main(data)