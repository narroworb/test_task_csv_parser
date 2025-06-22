import argparse
import csv

from tabulate import tabulate
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Простой CSV-фильтр и агрегатор")
    parser.add_argument("--file", help="Путь к CSV-файлу")
    parser.add_argument("--where", help='Фильтрация, например: "price>500"')
    parser.add_argument("--aggregate", help='Агрегация, например: "price=avg"')
    return parser.parse_args()


def load_csv(file_path: str) -> list[dict[str, str]]:
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def filter_data(data: list[dict[str, str]], condition: str | None) -> list[dict[str, str]]:
    if not condition:
        return data

    import re
    match = re.match(r"(.+?)([<>=])(.+)", condition.strip())
    if not match:
        raise ValueError("Некорректное условие фильтрации")

    col, op, value = match.groups()
    if col not in data[0]:
        raise ValueError(f"Колонка '{col}' не найдена в файле")
    value = value.strip()

    def match_row(row: str) -> bool:
        cell = row[col]
        try:
            cell = float(cell)
            value_cast = float(value)
        except ValueError:
            value_cast = value

        if op == ">":
            return cell > value_cast
        elif op == "<":
            return cell < value_cast
        elif op == "=":
            return cell == value_cast
        else:
            return False

    return [row for row in data if match_row(row)]


def aggregate_data(data: list[dict[str, str]], expression: str | None) -> None | str | dict[str, list[float]]:
    if not expression:
        return

    try:
        col, op = expression.split("=")
        col, op = col.strip(), op.strip().lower()
    except ValueError:
        raise ValueError("Агрегация должна быть в формате column=operation")

    if col not in data[0]:
        raise ValueError(f"Колонка '{col}' не найдена в файле")

    values = [float(row[col]) for row in data]

    if not values:
        return f"Нет данных для агрегации по колонке {col}"

    if op == "avg":
        result = sum(values) / len(values)
    elif op == "min":
        result = min(values)
    elif op == "max":
        result = max(values)
    else:
        raise ValueError(f"Агрегация {op} не поддерживается")
    return {op: [result]}


def main():
    args = parse_args()
    try:
        data = load_csv(args.file)
    except FileNotFoundError:
        print(f"Файл '{args.file}' не найден")
        sys.exit(1)

    try:
        data = filter_data(data, args.where)
        if args.aggregate:
            result = aggregate_data(data, args.aggregate)
            if isinstance(result, str):
                print(result)
            else:
                print(tabulate(result, headers="keys", tablefmt="grid"))
        else:
            print(tabulate(data, headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
