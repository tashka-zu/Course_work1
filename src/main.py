from src.reports import analyze_spending_by_category
from src.services import search_and_save_dataframe_to_json
from src.utils import load_excel_data
from src.views import main_views


def main():
    """Главная функция. Запускает все остальные функции и выдает результат в json файлах."""
    date_string = "11.07.2021 23:11:24"
    main_views(date_string)
    df = load_excel_data(input_file="../data/operations.xlsx")
    search_and_save_dataframe_to_json(df, "Магнит")
    analyze_spending_by_category(df, "Топливо", "30.07.2021")

if __name__ == "__main__":
    main()