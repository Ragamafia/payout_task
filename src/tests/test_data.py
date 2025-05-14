from unittest.mock import patch

from src.common import ReportBuilder
from src.reports import PayoutReportModule, Employer


def test_get_args_parser():
    parser = ReportBuilder().get_args_parser()
    args = parser.parse_args()
    test_file_dir = args.paths
    assert args.paths == test_file_dir
    return args.paths


@patch('glob.glob')
def test_get_csv_file(mock_glob):
    mock_glob.return_value = []
    builder = ReportBuilder()
    for i in mock_glob:
        result = builder._get_csv_files(test_get_args_parser())
        assert result == []


@patch('builtins.open')
@patch('csv.DictReader')
def test_parse_file(mock_dictreader, mock_open):
    data = []
    builder = ReportBuilder()
    files = builder._get_csv_files([])
    for file in files:
        data.append(builder._parse_file(file))

    for file in data:
        for i in file:
            assert isinstance(i, Employer)


@patch('glob.glob')
@patch('builtins.open')
@patch('csv.DictReader')
def test_full_flow(mock_dictreader, mock_open, mock_glob):

    builder = ReportBuilder()
    files = builder._get_csv_files(['C:\Python\PythonProjects\payout_task\data'])
    employers = []
    for i in files:
        employers.extend(builder._parse_file(i))

    assert len(employers) == 9
    return employers


def test_print_report(capfd):
    employers = test_full_flow()
    report_module = PayoutReportModule()
    printing = report_module.print_report(employers)
    out, err = capfd.readouterr()

    assert 'name' in out
