import pytest
from pathlib import Path

from src.cmd import ReportBuilder


def test_find_csv_files(temp_path):
    # Создаем временные файлы
    (temp_path / "file1.csv").write_text("data")
    (temp_path / "file2.csv").write_text("data")
    (temp_path / "not_csv.txt").write_text("data")

    files = ReportBuilder()._get_csv_files(str(temp_path))
    # Проверяем, что возвращаются только csv файлы
    assert len(files) == 2
    assert all(f.endswith('.csv') for f in files)


