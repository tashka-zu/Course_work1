from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import filter_data_by_date, load_excel_data


def test_load_excel_data_successfully(mocker):
    fake_data = pd.DataFrame(
        {"Номер карты": [123456, 789012], "Дата операции": ["01.01.2025 12:00:00", "02.01.2025 13:00:00"]}
    )

    mocker.patch("pandas.read_excel", return_value=fake_data)

    result = load_excel_data("path/to/file.xlsx")

    expected_data = fake_data.to_dict(orient="records")
    assert result == expected_data


def test_load_excel_data_fails_on_exception(mocker):
    mocker.patch("pandas.read_excel", side_effect=Exception("Excel reading error"))

    result = load_excel_data("path/to/file.xlsx")

    assert result == []


def test_filter_data_by_date(mocker):
    fake_data = pd.DataFrame(
        {"Номер карты": [123456, 789012], "Дата операции": ["01.01.2025 12:00:00", "02.01.2025 13:00:00"]}
    )

    mocker.patch("pandas.read_excel", return_value=fake_data)

    mocker.patch("pandas.to_datetime", side_effect=pd.to_datetime)

    m = mock_open()
    with patch("builtins.open", m):
        result_file = filter_data_by_date("01.01.2025 12:00:00")

    m.assert_called_with("../data/filtered_operations.json", "w", encoding="utf-8", errors="strict", newline="")
    assert result_file == "../data/filtered_operations.json"
