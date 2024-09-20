from datetime import datetime


def mask_card_number(card_number):
    """
    Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры.

    Args:
        card_number (str): Полный номер карты (16 цифр).

    Returns:
        str: Маскированный номер карты в формате XXXX XX** **** XXXX.
    """
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number):
    """
    Маскирует номер счета, показывая только последние 4 цифры.

    Args:
        account_number (str): Полный номер счета.

    Returns:
        str: Маскированный номер счета в формате **XXXX.
    """
    return f"**{account_number[-4:]}"


def format_date(date_str):
    """
    Преобразует строку даты из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_str (str): Дата в формате ISO (например, '2019-08-26T10:50:58.294041').

    Returns:
        str: Дата в формате ДД.ММ.ГГГГ.
    """
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")


def display_last_operations(operations):
    """
    Отображает 5 последних выполненных операций в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>

    Args:
        operations (list): Список операций, содержащий информацию о переводах.

    Работает с операциями, имеющими статус "EXECUTED", сортирует их по дате
    и выводит на экран данные по каждой операции, маскируя номера карт и счетов.
    """
    # Оставляем только выполненные операции и проверяем наличие ключа 'state'
    executed_operations = [op for op in operations if op.get("state") == "EXECUTED"]

    # Сортируем операции по дате в порядке убывания
    executed_operations.sort(key=lambda x: x["date"], reverse=True)

    # Берем последние 5 операций
    last_operations = executed_operations[:5]

    # Выводим информацию по каждой операции
    for operation in last_operations:
        date = format_date(operation["date"])
        description = operation["description"]
        amount = operation["operationAmount"]["amount"]
        currency = operation["operationAmount"]["currency"]["name"]
        from_account = operation.get("from", "")
        to_account = operation["to"]

        # Проверяем, есть ли данные в from_account и форматируем
        if from_account:
            if "Счет" in from_account:
                from_account = mask_account_number(from_account.split()[-1])
            else:
                from_account = mask_card_number(from_account.split()[-1])
        else:
            from_account = "Не указано"  # Если откуда-то перевод не указан

        # Маскируем номер счета назначения
        to_account = mask_account_number(to_account.split()[-1])

        # Печатаем данные
        print(f"{date} {description}")
        print(f"{from_account} -> {to_account}")
        print(f"{amount} {currency}\n")


# Пример использования функции:
import json

with open('operations.json', encoding='utf-8') as f:
    operations = json.load(f)

display_last_operations(operations)