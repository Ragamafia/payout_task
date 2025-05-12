import os
import glob
from argparse import ArgumentParser


class ReportModule:
    type: str
    name: str


class BaseReportModule(ReportModule):
    type: str = "base"
    name: str = "Базовый отчет"


class ReportBuilder:
    modules: list[ReportModule]
    parser: ArgumentParser

    def __init__(self):
        self.modules = [BaseReportModule()]
        self.parser = self.get_args_parser()

    def get_args_parser(self) -> ArgumentParser:
        report_types = ", ".join([f"'{m.type}'({m.name})" for m in self.modules])
        parser = ArgumentParser(
            description='Программа для вывода отчета из CSV файлов.')

        parser.add_argument(
            'paths',
            nargs='*',
            metavar='PATHS',
            help="Один или несколько путей к файлам или папкам. "
                 "Скрипт определит их тип."
        )
        parser.add_argument('--report',
                            type=str,
                            help=f'Выбор типа отчета: {report_types}')
        parser.add_argument('--json',
                            action='store_true',
                            help='Выводить отчет в формате JSON')
        parser.add_argument('--pattern',
                            type=str,
                            default='*.csv',
                            help='Шаблон для поиска файлов. По-умолчанию .csv.')

        return parser

    def _generate_config(self):
        args = self.parser.parse_args()

    def run(self):
        # дальше нам нужно наши аругменты которые мы получили на входе от юзера
        # засунуть в какой то конфиг. что бы дальше спокойно и удобно использовать.
        config = self._generate_config()


if __name__ == "__main__":
    ReportBuilder().run()