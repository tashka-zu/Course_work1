from unittest.mock import mock_open

import pytest

import src
from src.views import convert_valut, day_time, main_func_views, money_in_cards, stock_tracker


# Пример фикстуры для настройки начального состояния
@pytest.fixture
def setup_environment(mocker):
    # Мокируем внешние зависимости
    mocker.patch("src.views.requests.get")
    mocker.patch("builtins.open", new_callable=mock_open)


def test_stock_tracker_success(mocker):
    # Устанавливаем ожидаемый ответ для requests.get
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"Global Quote": {"05. price": "150"}}
    mock_response.status_code = 200
    mocker.patch("src.views.requests.get").return_value = mock_response

    # Устанавливаем ожидаемое значение для convert_valut
    mocker.patch("src.views.convert_valut", return_value=15000)

    # Устанавливаем список тикеров
    mocker.patch("src.views.tickers", ["AAPL"])

    result = stock_tracker()
    assert result == [{"stock": "AAPL", "price": 15000}]


def test_convert_valut_success(mocker):
    # Устанавливаем ожидаемый ответ для requests.get
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"conversion_rates": {"RUB": 90}}
    mock_response.status_code = 200
    mocker.patch("src.views.requests.get").return_value = mock_response

    result = convert_valut(100, "USD", "RUB")
    assert result == 9000


def test_day_time_morning(mocker):
    # Мокируем текущее время
    mocker.patch("src.views.datetime.datetime")
    src.views.datetime.datetime.now.return_value.hour = 10

    result = day_time()
    assert result == "Доброе утро"


def test_money_in_cards():
    operation_info = [
        {"Номер карты": "1234567890123456", "Сумма операции с округлением": -1000},
        {"Номер карты": "1234567890123456", "Сумма операции с округлением": -2000},
    ]

    result = money_in_cards(operation_info)
    assert result == {"3456": {"sum": -3000}}


def test_main_func_views(mocker):
    # Мокируем функции, которые используются в main_func_views
    mocker.patch("src.views.filter_data_by_date", return_value="../data/filtered_operations.json")
    mocker.patch(
        "src.views.load_json_data",
        return_value=[{"Номер карты": "1234567890123456", "Сумма операции с округлением": -1000}],
    )
    mocker.patch("src.views.day_time", return_value="Доброе утро")
    mocker.patch("src.views.money_in_cards", return_value={"3456": {"sum": -1000}})
    mocker.patch("src.views.top_5_trans", return_value=[])
    mocker.patch("src.views.convert_valut", return_value=75)
    mocker.patch("src.views.stock_tracker", return_value=[{"stock": "AAPL", "price": 15000}])

    # Мокируем функцию open для записи JSON
    mocked_open = mock_open()
    mocker.patch("builtins.open", mocked_open)

    # Вызываем основную функцию
    main_func_views("01.01.2025 12:00:00")

    # Проверяем, что файл был записан
    mocked_open.assert_called_with("../data/report.json", "w", encoding="utf-8")
