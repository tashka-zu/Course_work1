import logging
import os
from datetime import datetime
from functools import wraps

import pandas as pd

#Настройки логирования
log_directory = "../logs"
os.makedirs(log_directory, exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_directory, "search.log"), mode="w", encoding="utf-8")


formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

# Декоратор для записи результата выполнения функции в JSON файл
def log_result_to_file(file_name):
    """Декоратор, который записывает результат выполнения функции в указанный JSON файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Обертка для функции, которая логирует выполнение и записывает результат в JSON файл"""
            try:

                logger.info(f"Выполнение функции: {func.__name__}")

                df = func(*args, **kwargs)

                if isinstance(df, pd.DataFrame):
                    df.to_json(file_name, orient="records", lines=True, force_ascii=False)
                    logger.info(f"Результат функции записан в файл: {file_name}")
                else:
                    return df

            except Exception as e:
                logger.error(f"Ошибка при выполнении функции {func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


# Функция для анализа трат по категории
@log_result_to_file("../report_decor.json")
def analyze_spending_by_category(transactions, category, date=None) -> pd.DataFrame:
    """
     В функцию подаются датафрейм, категория и дата. В результате функция возвращает JSON-файл,
     содержащий данные о расходах в указанной категории.
    """
    try:
        logger.info(f"Запрос для категории: {category} с датой: {date}")

        if not date:
            stop_date = datetime.now()
        else:
            stop_date = datetime.strptime(date, "%d.%m.%Y")
            stop_date = stop_date.replace(hour=0, minute=0, second=0, microsecond=0)

        logger.info("Определение даты, начиная с которой будут взяты операции для подсчета трат по категориям")

        start_date = stop_date - pd.Timedelta(days=90)

        logger.info("Проверка на наличие необходимых столбцов в датафрейм")

        required_columns = ["Дата платежа", "Категория", "Сумма операции"]

        if isinstance(transactions, list):
            transactions = pd.DataFrame(transactions)

        for column in required_columns:
            if column not in transactions.columns:
                logger.error(f"Отсутствует необходимый столбец: {column}")
                return pd.DataFrame()

        logger.info("Преобразование дат операций в объект datatime")

        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", errors="coerce")

        logger.info("Формирование списка операций для формирования отчета")

        logger.debug(f"Фильтруемый датафрейм:\n{transactions}")

        filtered_transactions = transactions[
            (transactions["Дата платежа"] >= start_date)
            & (transactions["Дата платежа"] <= stop_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма операции"] < 0)
        ]

        logger.debug(f"Отфильтрованные данные:\n{filtered_transactions}")

        logger.info("Инициализация отчета")

        total_spending = filtered_transactions["Сумма операции"].abs().sum()

        result = pd.DataFrame({"Категория": [category], "Сумма трат": [total_spending]})

        logger.info(f"Результаты для категории '{category}': {total_spending} руб.")
        return result

    except ValueError as ve:
        logger.error(f"Ошибка значения: {ve}")
        return pd.DataFrame()

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return pd.DataFrame()


# trans = read_xlsx("../data/operations.xlsx")
# spending_by_category(trans, "Супермаркеты", "30.11.2019")