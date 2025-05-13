import pytest

from src.cmd import ReportBuilder


def run(self):
    config = self._generate_config()

    for i in config.files:
        config.module.print_report(self._parse_file(i))

@pytest.fixture()
def testing_fun():
    ReportBuilder().run()

def test_fun(testing_fun):
    assert testing_fun



