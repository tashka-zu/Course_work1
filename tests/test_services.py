import json
import pandas as pd
from src.services import search_and_save_dataframe_to_json

example_data = pd.DataFrame(
    {
        "Категория": [
            "Магазин 1",
            "Магазин 2",
        ],
        "Описание": ["Покупка продуктов", "Оплата услуг"],
        "Сумма": [1000, 500],
    }
)

def test_re_sort_with_valid_data():
    result_file = search_and_save_dataframe_to_json(example_data, "Маг", output_file="search_results.json")

    assert result_file == "search_results.json"

    with open(result_file, "r") as f:
        result = json.load(f)

    assert len(result) == 2
    for res in result:
        if res.get("Категория") == "Магазин 1":
            assert res.get("Категория") == "Магазин 1"
        elif res.get("Категория") == "Магазин 2":
            assert res.get("Категория") == "Магазин 2"
        else:
            break

def test_re_sort_with_empty_data():
    df = pd.DataFrame()

    result_file = search_and_save_dataframe_to_json(df, "Маг", output_file="empty_search_results.json")

    assert result_file == "empty_search_results.json"

    with open(result_file, "r") as f:
        result = json.load(f)

    assert result == []

def test_re_sort_with_no_matching_data():
    df = pd.DataFrame(
        {
            "Категория": [
                "Ресторан 1",
                "Ресторан 2",
            ],
            "Описание": ["Обед", "Ужин"],
            "Сумма": [2000, 1500],
        }
    )

    result_file = search_and_save_dataframe_to_json(df, "Маг", output_file="no_match_search_results.json")

    assert result_file == "no_match_search_results.json"

    with open(result_file, "r") as f:
        result = json.load(f)

    assert result == []
