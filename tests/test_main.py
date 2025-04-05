from unittest.mock import MagicMock, patch

from src.main import main


@patch("src.main.main_func_views")
@patch("src.main.load_excel_data")
@patch("src.main.search_and_save_dataframe_to_json")
@patch("src.main.analyze_spending_by_category")
def test_main(mock_analyze, mock_search_and_save, mock_load_excel, mock_main_func_views):
    # Настраиваем моки для возврата фиктивных данных
    mock_load_excel.return_value = MagicMock()  # Возвращаем фиктивный DataFrame

    # Вызываем основную функцию
    main()

    # Проверяем, что все функции были вызваны с правильными параметрами
    mock_main_func_views.assert_called_once_with("11.07.2021 23:11:24")
    mock_load_excel.assert_called_once_with(input_file="../data/operations.xlsx")
    mock_search_and_save.assert_called_once_with(mock_load_excel.return_value, "Магнит")
    mock_analyze.assert_called_once_with(mock_load_excel.return_value, "Топливо", "30.07.2021")
