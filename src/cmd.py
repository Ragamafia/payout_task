from pathlib import Path
from dataclasses import dataclass
from argparse import ArgumentParser

from src.config import cfg


@dataclass
class Employer:
    id: int
    email: str
    name: str
    department: str
    hours_worked: int
    rate: int

class ReportModule:
    type: str
    name: str

    def print_report(self, employers: list[Employer], json: bool = False):
        ...


class PayoutReportModule(ReportModule):
    type: str = "payout"
    name: str = "Отчет по зарплате"

    def print_report(self, files: list[Employer], json: bool = False):
        print(f"{'name':>19} {'hours':>18} {'rate':>10} {'payout':>13}")
        departments = []
        total_cash = []
        total_hours = []

        for employee in files:

            if employee.department not in departments:
                departments.append(employee.department)
                print(employee.department)

            cash = int(employee.rate) * int(employee.hours_worked)

            print(f"{' ':->14}",
                  f"{employee.name:<18}",
                  f"{employee.hours_worked:<12}",
                  f"{employee.rate:<10}",
                  f"${str(cash):<10}"
                  )

            total_cash.append(cash)
            total_hours.append(int(employee.hours_worked))

        print(f"{str(sum(total_hours)):>37}",
              f"{'$' + str(sum(total_cash)):>25}"
              )
        print(f"{'':->65}")


@dataclass
class Config:
    module: ReportModule
    files: list[Path]
    json: bool = False


class ReportBuilder:
    modules: list[ReportModule]
    parser: ArgumentParser

    def __init__(self):
        self.modules = [PayoutReportModule()]
        self.parser = self.get_args_parser()

    def _get_modules_string(self):
        return ", ".join([f"'{m.type}'({m.name})" for m in self.modules])

    def get_args_parser(self) -> ArgumentParser:
        modules_string = self._get_modules_string()
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
                            default=cfg.DEFAULT_REPORT_TYPE,
                            help=f'Выбор типа отчета: например {modules_string}')
        parser.add_argument('--json',
                            action='store_true',
                            help='Выводить отчет в формате JSON')
        parser.add_argument('--recursive',
                            action='store_true',
                            default=cfg.DEFAULT_RECURSIVE,
                            help='Рекурсивный поиск (по-умолчанию)')

        return parser

    def _get_module_by_type(self, type: str) -> ReportModule | None:
        for module in self.modules:
            if module.type == type:
                return module

    def _generate_config(self) -> Config:
        args = self.parser.parse_args()

        module = self._get_module_by_type(args.report)
        if not module:
            modules = self._get_modules_string()
            raise ValueError(f"invalid report type. valid types: {modules}")

        files = self._get_csv_files(args.paths, recursive=args.recursive)
        if not files:
            raise ValueError("no valid csv files found")

        return Config(
            files=files,
            module=module,
            json=args.json
        )

    def _get_csv_files(self, paths: list[str | Path], recursive: bool = True):
        csv_files = []

        for path in paths:
            path = Path(path) if isinstance(path, str) else path
            if path.is_file() and path.suffix == '.csv':
                csv_files.append(path)
            elif path.is_dir() and recursive:
                paths = list(path.glob('**/*.csv'))
                csv_files.extend(self._get_csv_files(paths, recursive=True))

        return csv_files

    def _parse_file(self, file: Path)-> list[Employer]:
        employers = []
        with file.open() as csv_file:
            rows = [l.strip().split(',') for l in csv_file.readlines()]
            headers, *rows = rows
            for row in rows:
                raw = dict(zip(headers, row))

                validated = {}
                for k, v in raw.items():
                    if k in cfg.RATE_ALIASES:
                        validated['rate'] = v
                    else:
                        validated[k] = v

                employer = Employer(**validated)
                employers.append(employer)
                #return employer

        return employers

    def run(self):
        config = self._generate_config()

        for i in config.files:
            config.module.print_report(self._parse_file(i))
