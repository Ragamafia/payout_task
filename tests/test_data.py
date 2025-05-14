import pytest
from unittest.mock import patch, MagicMock
import os


from cmd import ReportBuilder, PayoutReportModule, Employer


def test_get_args_parser():
    parser = ReportBuilder().get_args_parser()
    args = parser.parse_args(['some_path'])
    assert args.path == 'some_path'

@patch('glob.glob')
def test_get_csv_file(mock_glob):
    mock_glob.return_value = ['data1.csv', 'data2.csv']
    builder = ReportBuilder()
    result = builder._get_csv_files(['some_dir'])
    assert result == ['data1.csv', 'data2.csv']
    mock_glob.assert_called_with(os.path.join('some_dir', '*.csv'))

@patch('builtins.open')
@patch('csv.DictReader')
def test_parse_file(mock_dictreader, mock_open):
    mock_open.return_value.__enter__.return_value = None
    mock_dictreader.returt_value = [
        {'id': '', 'email': '', 'name': 'Иван', 'department': '', 'hours_worked': '', 'rate': 300}
    ]

    builder = ReportBuilder()
    result = builder._parse_file('dummy_path')

    assert len(result) == 2
    assert isinstance(result[0], Employer)
    assert result[0].name == 'Karen Withe'
    assert result[0].rate == 300

@patch('glob.glob')
@patch('builtins.open')
@patch('csv.DictReader')
def test_full_flow(mock_dictreader, mock_open, mock_glob):
    mock_glob.return_value = ['data1.csv']
    mock_dictreader.returt_value = [
        {'id': '', 'email': '', 'name': 'Karen White', 'department': '', 'hours_worked': '', 'rate': 300}
    ]

    builder = ReportBuilder()
    files = builder._get_csv_files(['some_dir'])

    employers = []
    for i in files:
        employers.extend(builder._parse_file(i))

    assert len(employers) == 2

def test_print_report(capsys):
    from src.cmd import Employer, PayoutReportModule

    employers = [
        Employer(id=201, email='karen@example.com', name='Karen White', department='Sales', hours_worked=165, rate=50)
    ]

    report_module = PayoutReportModule()
    report_module.print_report(employers)
    captured = capsys.readouterr()

    assert 'Отчет по зарплате' in captured.out
    assert 'Karen White' in captured.out
