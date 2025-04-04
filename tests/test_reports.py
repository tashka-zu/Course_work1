import json
import pandas as pd
import pytest

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
    with open("../Course_work1/report_decor.json", "r", encoding="utf-8") as file:
        data_from_file = json.load(file)

    actual_result = pd.DataFrame(data_from_file, columns=["Категория", "Сумма трат"])
    actual_result = actual_result[actual_result["Категория"] == "Еда"]

    pd.testing.assert_frame_equal(actual_result.reset_index(drop=True), expected.reset_index(drop=True))

@pytest.mark.parametrize(
    "expected",
    [
        pd.DataFrame({"Категория": ["Такси"], "Сумма трат": [2089]}),
    ],
)
def test_spending_by_category_taxi(transactions, expected):
    with open("../Course_work1/report_decor.json", "r", encoding="utf-8") as file:
        data_from_file = json.load(file)

    actual_result = pd.DataFrame(data_from_file, columns=["Категория", "Сумма трат"])
    actual_result = actual_result[actual_result["Категория"] == "Такси"]

    pd.testing.assert_frame_equal(actual_result.reset_index(drop=True), expected.reset_index(drop=True))