import json
import logging
import re

import pandas as pd

# Настройки логирования
logging.basicConfig(
    filename="../logs/search.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
    encoding="utf-8",
    force=True,
)


# Функция для поиска совпадений
def search_and_save_dataframe_to_json(df, search, output_file="../data/search_results.json"):
    """Функция для поиска совпадений в DataFrame по заданному шаблону"""
    logging.info(f"Начат поиск по DataFrame с критерием поиска: {search}")

    if isinstance(df, list):
        df = pd.DataFrame(df)

    if df is None or df.empty:
        logging.warning("DataFrame пуст или не загружен.")
        result = []
    else:
        if not isinstance(df, pd.DataFrame):
            logging.error(f"Ошибка: передан не DataFrame, а {type(df)}.")
            raise ValueError("Функция re_sort ожидает DataFrame.")

        df = df.fillna(0)

        list_transactions = df.to_dict(orient="records")
        pattern = re.compile(search, re.IGNORECASE)

        result = [
            operation
            for operation in list_transactions
            if pattern.search(str(operation.get("Категория", "")))
            or pattern.search(str(operation.get("Описание", "")))
        ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    logging.info(f"Результат ({len(result)} совпадений) записан в {output_file}.")

    return output_file
