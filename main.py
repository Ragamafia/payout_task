import os

from read import is_csv_file, read_csv_file


def main():
    while True:
        file_path = input('Please, input path for CSV file: ')

        if not os.path.isfile(file_path):
            print('File defined. Enter correct path. ')
            continue

        if not is_csv_file(file_path):
            print('This file not CSV.')
            continue

        data = read_csv_file(file_path)

        if data is not None:
            print('Data:')
            for row in data:
                print(row)
            break


if __name__ == "__main__":
    main()