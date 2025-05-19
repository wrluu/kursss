import logging
from datetime import datetime
from typing import Optional

import pandas as pd

from logging_config import setup_logging
from settings import REPORTS_PATH
from src.decorators import decorator_record_file

setup_logging()
logger = logging.getLogger("my_log")


@decorator_record_file(REPORTS_PATH)
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает на вход датафрейм с транзакциями, название категории, и опциональную дату в формате ДД.ММ.ГГГГ.
    Если дата не передана, то берется текущая дата.
    """
    try:
        if date:
            stop_date = datetime.strptime(date, "%d.%m.%Y")
            start_date = stop_date - pd.Timedelta(days=90)
        else:
            start_date = min(transactions['Дата платежа'])
            stop_date = max(transactions['Дата платежа'])

        required_columns = ['Дата платежа', 'Категория', 'Сумма операции']
        for column in required_columns:
            if column not in transactions.columns:
                return pd.DataFrame()

        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

        filtered_transactions = transactions[
            (transactions["Дата платежа"] >= start_date) &
            (transactions["Дата платежа"] <= stop_date) &
            (transactions["Категория"] == category) &
            (transactions["Сумма операции"] < 0)]

        total_spending = filtered_transactions["Сумма операции"].abs().sum()
        result = pd.DataFrame({
            "Категория": [category],
            "Сумма трат": [total_spending]
        })
    except ValueError as ve:
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
    return result