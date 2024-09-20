import pytest
from main import mask_card_number, mask_account_number, format_date, display_last_operations


# Тест для функции маскировки номера карты
def test_mask_card_number():
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert mask_card_number("9876543210987654") == "9876 54** **** 7654"


# Тест для функции маскировки номера счета
def test_mask_account_number():
    assert mask_account_number("1234567890") == "**7890"
    assert mask_account_number("0987654321") == "**4321"


# Тест для функции форматирования даты
def test_format_date():
    assert format_date("2019-08-26T10:50:58.294041") == "26.08.2019"
    assert format_date("2018-07-03T18:35:29.512364") == "03.07.2018"


# Тест для функции отображения операций (используем подмену вывода через capsys)
def test_display_last_operations(capsys):
    operations = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
    ]

    display_last_operations(operations)

    # Захватываем вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод правильный
    assert "26.08.2019 Перевод организации" in captured.out
    assert "1596 83** **** 5199 -> **9589" in captured.out
    assert "31957.58 руб." in captured.out

    assert "03.07.2019 Перевод организации" in captured.out
    assert "7158 30** **** 6758 -> **5560" in captured.out
    assert "8221.37 USD" in captured.out
