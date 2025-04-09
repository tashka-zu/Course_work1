import json
import logging

import pandas as pd


def load_excel_data(input_file="../data/operations.xlsx"):
    """Загружает данные из Excel файла и возвращает список словарей"""
    try:
        df = pd.read_excel(input_file, engine="openpyxl")

        df = df.dropna(subset=["Номер карты"])

        data = df.to_dict(orient="records")

        logging.info(f"Successfully read the file: {input_file}, {len(data)} rows loaded.")
        return data
    except Exception as e:
        logging.error(f"Error reading xlsx file {input_file}: {e}")
        return []


def load_json_data(file_path):
    """Загружает данные из JSON файла и возвращает список словарей"""
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return []


# Фильтрует данные из Excel файла
def filter_data_by_date(
    date_str, input_file="../data/operations.xlsx", output_file="../data/filtered_operations.json"
):
    """Фильтрует данные из Excel файла по дате и сохраняет результаты в новый JSON файл"""
    df = pd.read_excel(input_file, engine="openpyxl")
    df.dropna(subset=["Номер карты"])
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")
    target_date = pd.to_datetime(date_str, dayfirst=True, format="%d.%m.%Y %H:%M:%S")
    start_of_month = target_date.replace(day=1)
    filtered_df = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= target_date)]
    sorted_filtered_df = filtered_df.sort_values(by=["Дата операции"])
    sorted_filtered_df["Дата операции"] = sorted_filtered_df["Дата операции"].dt.strftime("%d-%m-%Y %H:%M:%S")
    sorted_filtered_df.to_json(output_file, orient="records", force_ascii=False, indent=4)

    return output_file
