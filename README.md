# Course work

Это приложение для анализа транзакций, которые находятся в Excel-файле. Приложение генерирует JSON-данные для веб-страниц, формировует Excel-отчеты, а также предоставляет другие сервисы.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш_репозиторий.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd ваш_проект
   ```
3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

Пример функции в модуле main.py:

```python
from src.reports import analyze_spending_by_category
from src.services import search_and_save_dataframe_to_json
from src.utils import load_excel_data
from src.views import main_func_views


def main():
    """Главная функция. Запускает все остальные функции и выдает результат в json файлах."""
    date_string = "11.07.2021 23:11:24"
    main_func_views(date_string)
    df = load_excel_data(input_file="../data/operations.xlsx")
    search_and_save_dataframe_to_json(df, "Магнит")
    analyze_spending_by_category(df, "Топливо", "30.07.2021")

if __name__ == "__main__":
    main()
```

## Тестирование

В нашем проекте я использую тестирование для корректности работы. Я использовала фреймвор pytest.
Все написанные тесты находятся в папке tests.

```
File	           statements missing excluded coverage
src\__init__.py	        0	     0	      0	     100%
src\main.py            12	     1	      0	      92%
src\reports.py	       60	    11	      0       82%
src\services.py	       23	     3	      0	      87%
src\utils.py	       31	     6	      0	      81%
src\views.py	      114	    28	      0	      75%
Total	              240	    49	      0	      80%
```