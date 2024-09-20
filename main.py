from datetime import datetime


def mask_card_number(card_number):
    # Преобразуем номер карты в формат XXXX XX** **** XXXX
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number):
    # Преобразуем номер счета в формат **XXXX
    return f"**{account_number[-4:]}"


def format_date(date_str):
    # Преобразуем дату в формат ДД.ММ.ГГГГ
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")


def display_last_operations(operations):
    # Оставляем только выполненные операции
    executed_operations = [op for op in operations if op["state"] == "EXECUTED"]

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

        # Маскируем номера карт и счетов
        if "Счет" in from_account:
            from_account = mask_account_number(from_account.split()[-1])
        else:
            from_account = mask_card_number(from_account.split()[-1])

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
