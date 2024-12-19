import unittest

# Импортируем функции из вашего кода
from translator import validate_name, process_json_data, process_expression, json_to_custom_language


class TestValidateName(unittest.TestCase):
    def test_valid_names(self):
        # Корректные имена
        validate_name("VALID_NAME")  # Не должно выдать исключений
        validate_name("A")  # Однобуквенное имя
        validate_name("THIS_IS_CORRECT")

    def test_invalid_names(self):
        # Некорректные имена
        with self.assertRaises(ValueError):
            validate_name("InvalidName")  # Содержит строчные буквы
        with self.assertRaises(ValueError):
            validate_name("INVALID-NAME")  # Содержит недопустимый символ
        with self.assertRaises(ValueError):
            validate_name("")  # Пустая строка
        with self.assertRaises(ValueError):
            validate_name("123INVALID")  # Начинается с цифры


class TestProcessJsonData(unittest.TestCase):
    def test_process_simple_dict(self):
        input_data = {
            "name": "value",
            "number": 42,
            "nested": {"key": "another_value"}
        }
        expected_data = {
            "NAME": "value",
            "NUMBER": 42,
            "NESTED": {"KEY": "another_value"},
        }
        result = process_json_data(input_data)
        self.assertEqual(result, expected_data)

    def test_process_list(self):
        input_data = ["value", {"key": "another_value"}]
        expected_data = ["value", {"KEY": "another_value"}]
        result = process_json_data(input_data)
        self.assertEqual(result, expected_data)


class TestProcessExpression(unittest.TestCase):
    def test_valid_expression(self):
        constants = {"CONST": 10, "VALUE": 20}
        self.assertEqual(process_expression("?[CONST + 5]", constants), 15)
        self.assertEqual(process_expression("?[VALUE + 10]", constants), 30)

    def test_invalid_expression(self):
        constants = {"CONST": 10}
        with self.assertRaises(ValueError):
            process_expression("?[UNKNOWN + 1]", constants)  # Неизвестная константа

        with self.assertRaises(ValueError):
            process_expression("?[]", constants)  # Пустое выражение

        with self.assertRaises(ValueError):
            process_expression("?[CONST - 5]", constants)  # Некорректное выражение


class TestJsonToCustomLanguage(unittest.TestCase):

    def test_nested_data(self):
        input_data = {
            "TABLE": {
                "SUB_TABLE": {
                    "VALUE": 5
                }
            }
        }

        # Обработка данных перед вызовом json_to_custom_language
        processed_data = process_json_data(input_data)

        result = json_to_custom_language(processed_data)

        expected_result = (
            "TABLE(\n"
            "  SUB_TABLE => temp(\n"
            "  VALUE => 5,\n"
            "),\n"
            ")"
        )

        # Печать для отладки
        if result != expected_result:
            print("\nGenerated Result:")
            print(result)
            print("\nExpected Result:")
            print(expected_result)

        # Сравнение результатов без лишних пробелов и в верхнем регистре
        self.assertEqual(result.strip(), expected_result.strip())

    def test_simple_data(self):
        input_data = {
            "CONST": 10,
            "TABLE": {
                "KEY1": 1,
                "KEY2": "value"
            }
        }
        processed_data = process_json_data(input_data)
        result = json_to_custom_language(processed_data)
        expected_result = (
            "CONST is 10;\n"
            "TABLE(\n"
            "  KEY1 => 1,\n"
            "  KEY2 => 'value',\n"
            ")"
        )
        self.assertEqual(result, expected_result)






if __name__ == "__main__":
    unittest.main()
