import json
import re
import argparse


def validate_name(name, is_top_level=True):
    """
    Проверяет, соответствует ли имя правилам:
    - Состоит только из заглавных букв (A-Z) и символов подчеркивания (_).
    """
    # Проверка только для имен на верхнем уровне (первого уровня)
    if is_top_level:
        if not re.fullmatch(r"[A-Z_]+", name):
            raise ValueError(f"Некорректное имя: {name}")


def process_json_data(data, constants=None, is_top_level=True):
    """
    Рекурсивно обрабатывает данные, преобразуя все имена в верхний регистр.
    Также проверяет корректность имен с помощью validate_name.
    """
    if constants is None:  # Инициализация словаря констант
        constants = {}

    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            upper_key = key.upper()  # Преобразуем ключ в верхний регистр
            validate_name(upper_key, is_top_level)  # Проверяем имя на верхнем уровне

            # Если значение - это число, сохраняем его как константу
            if isinstance(value, int) and is_top_level:
                constants[upper_key] = value

            # Рекурсивно обрабатываем вложенные данные
            result[upper_key] = process_json_data(value, constants, is_top_level=False)
        return result
    elif isinstance(data, list):
        return [process_json_data(item, constants, is_top_level) for item in data]
    else:
        return data  # Если значение не словарь или список, просто возвращаем его



def process_expression(expression, constants):
    """
    Обрабатывает выражения в формате "?[CONSTANT + 1]" и вычисляет их.
    """
    if expression.startswith("?[") and expression.endswith("]"):
        expr = expression[2:-1]
        parts = expr.split('+')
        if len(parts) == 2:
            var = parts[0].strip()
            num = int(parts[1].strip())
            if var in constants:
                return constants[var] + num
            else:
                raise ValueError(f"Неизвестная константа: {var}")
        else:
            raise ValueError("Некорректное выражение.")
    return expression


def json_to_custom_language(data):
    """
    Преобразует данные JSON в формат учебного конфигурационного языка.
    """
    constants = {}
    result = []


    # Обработка констант
    for key, value in data.items():
        key = key.upper()  # Убедимся, что имя в верхнем регистре
        validate_name(key)  # Проверяем имя

        if isinstance(value, int):
            # Собираем константы
            constants[key] = value
            result.append(f"{key} is {value};")

    # Обработка таблицы и вложенной структуры
    for key, value in data.items():
        if isinstance(value, dict):
            table_result = f"{key}(\n"
            for sub_key, sub_value in value.items():
                sub_key = sub_key.upper()
                if isinstance(sub_value, int):
                    table_result += f"  {sub_key} => {sub_value},\n"
                elif isinstance(sub_value, str):
                    # Обработка строк / выражений
                    sub_value = process_expression(sub_value, constants)
                    table_result += f"  {sub_key} => '{sub_value}',\n"
                elif isinstance(sub_value, dict):
                    table_result += f"  {sub_key} => {json_to_custom_language({'temp': sub_value})},\n"
            table_result += ")"
            result.append(table_result)

    return "\n".join(result)


def main():
    # Создание парсера аргументов
    parser = argparse.ArgumentParser(description="Конфигурационный язык транслятор")
    parser.add_argument("input_file", help="Путь к входному JSON файлу")
    parser.add_argument("output_file", help="Путь к выходному файлу для сохранения результата")

    # Парсим аргументы командной строки
    args = parser.parse_args()

    # Чтение входного файла
    try:
        with open(args.input_file, 'r') as infile:
            input_data = infile.read()

        # Загружаем JSON
        data = json.loads(input_data)

        # Обрабатываем данные и преобразуем в формат конфигурационного языка
        processed_data = process_json_data(data)

        # Преобразуем данные в строку с конфигурационным языком
        config_str = json_to_custom_language(processed_data)

        # Сохраняем результат в выходной файл
        with open(args.output_file, "w") as output_file:
            output_file.write(config_str)

        print(f"Вывод сохранен в файл {args.output_file}")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except FileNotFoundError:
        print("Ошибка: Входной файл не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
