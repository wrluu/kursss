from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import get_json_currencies, get_json_stocks, get_xlsx


@patch("pandas.read_excel")
def test_get_xlsx(mock_read_excel, operations_from_excel, operations_list_valid):
    mock_read_excel.return_value = pd.DataFrame(operations_from_excel)
    result = get_xlsx("valid/path/to/file")
    assert operations_list_valid in result


def test_get_xlsx_empty_path():
    result = get_xlsx("")
    assert [] in result


@patch("pandas.read_excel")
def test_get_xlsx_empty_file(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame()
    result = get_xlsx("valid/path/to/file")
    assert [] in result


def test_get_xlsx_invalid_path():
    result = get_xlsx("invalid/path/to/file")
    assert [] in result


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}""",
)
def test_get_json_currencies(mock_file):
    result = get_json_currencies("some/path")
    assert result == ["USD", "EUR"]
    mock_file.assert_called_with("some/path", "r", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open, read_data="")
def test_get_json_currencies_invalid(mock_file):
    with pytest.raises(Exception) as exc_info:
        get_json_currencies("some/path")
    assert "Ошибка при чтении файла:" in str(exc_info.value)


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""{"key": ["value_1", "value_2"], "key_2": ["value_3", "value_4"]}""",
)
def test_get_json_currencies_not_key(mock_file):
    result = get_json_currencies("some/path")
    assert result == []


def test_get_json_currencies_not_path():
    with pytest.raises(Exception) as exc_info:
        get_json_currencies("")
    assert "Ошибка при чтении файла:" in str(exc_info.value)


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}""",
)
def test_get_json_stocks(mock_file):
    result = get_json_stocks("some/path")
    assert result == ["AAPL", "AMZN"]


def test_get_json_stocks_not_path():
    with pytest.raises(Exception) as exc_info:
        get_json_stocks("")
    assert "Ошибка при чтении файла:" in str(exc_info.value)


@patch("builtins.open", new_callable=mock_open, read_data="////")
def test_get_json_stocks_invalid(mock_file):
    with pytest.raises(ValueError) as exc_info:
        get_json_stocks("some/path")
    assert "Ошибка при чтении файла:" in str(exc_info.value)