from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.reports import analyze_spending_by_category


@pytest.fixture(scope="module")
def transactions():
    return pd.DataFrame(
        {
            "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
            "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
            "Сумма операции": [-777, -555, -1312, -666],
        }
    )


@pytest.mark.parametrize(
    "expected",
    [
        pd.DataFrame({"Категория": ["Еда"], "Сумма трат": [555]}),
    ],
)
def test_spending_by_category_food(transactions, expected):
    with patch("builtins.open", mock_open()):
        result = analyze_spending_by_category(transactions, "Еда", "01.01.2025")
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_spending_by_category_no_data(transactions):
    with patch("builtins.open", mock_open()):
        result = analyze_spending_by_category(transactions, "Несуществующая категория", "01.01.2025")
        expected_result = pd.DataFrame(
            {"Категория": pd.Series([], dtype="object"), "Сумма трат": pd.Series([], dtype="object")}
        )
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result.reset_index(drop=True))


def test_spending_by_category_invalid_date(transactions):
    # Проверяем сценарий с некорректной датой
    with patch("builtins.open", mock_open()):
        result = analyze_spending_by_category(transactions, "Еда", "invalid_date")
        if result is not None:
            assert result.empty
        else:
            pytest.fail("Функция возвращет значение None, когда ожидается Data Frame")
