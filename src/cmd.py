import os
import glob
import argparse

from src.read import is_csv_file, read_csv_file


def parse_input():
    data = []

    parser = argparse.ArgumentParser(description='Программа для вывода отчета из CSV файлов.')

    parser.add_argument('directory', type=str, help='Путь к CSV файлу.')
    parser.add_argument(
        'paths',
        nargs='*',
        metavar='PATHS',
        help="Один или несколько путей к файлам или папкам. Скрипт определит их тип."
    )
    parser.add_argument('--report', type=str, help='Выбор типа отчета (например "payout")')
    parser.add_argument('--json', action='store_true', help='Выводить отчет в формате JSON')
    parser.add_argument('--pattern', type=str, default='*.csv', help='Шаблон для поиска файлов. По-умолчанию .csv.')

    args = parser.parse_args()
    search_pattern = os.path.join(args.directory, args.pattern)
    files = glob.glob(search_pattern)

    if not files:
        print("Файлы не найдены в выбранном формате.")
        return

    for file in files:
        data.append(read_csv_file(file))

    print(f"Тип отчета: {args.report}")
    return data
