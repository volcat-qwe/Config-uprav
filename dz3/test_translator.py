import unittest
import subprocess

class TestConfigLanguage(unittest.TestCase):

    def run_translator(self, input_data):
        # Преобразуем входные данные в строку (если они не в строковом формате)
        result = subprocess.run(
            ['python3', 'translator.py'],
            input=input_data,  # передаем строковые данные напрямую
            capture_output=True,
            text=True  # Указываем, что вывод и ввод текстовые (не байтовые)
        )
        return result.stdout

    def test_db_config(self):
        input_data = '''{
            "DB_CONFIG": {
                "MAX_CONNECTIONS": 100,
                "TABLES": {
                    "USERS": {
                        "ID": 1,
                        "NAME": "'John'",
                        "AGE": 30
                    },
                    "ORDERS": {
                        "ORDER_ID": 101,
                        "USER_ID": 1,
                        "TOTAL": 50
                    }
                },
                "INDEX_SIZE": "?[MAX_CONNECTIONS * 10]"
            },
            "SYSTEM_VERSION": 1,
            "EXPR": "?[SYSTEM_VERSION + 1]"
        }'''
        output = self.run_translator(input_data)

        expected_output = '''DB_CONFIG(
    MAX_CONNECTIONS => 100,
    TABLES => temp(
        USERS => temp(
            ID => 1,
            NAME => 'John',
            AGE => 30,
        ),
        ORDERS => temp(
            ORDER_ID => 101,
            USER_ID => 1,
            TOTAL => 50,
        ),
    ),
    INDEX_SIZE is 1000;
)
SYSTEM_VERSION is 1;
EXPR is 2;
'''
        self.assertEqual(output, expected_output)

    def test_web_server_config(self):
        input_data = '''{
            "SERVER_CONFIG": {
                "MAX_THREADS": 8,
                "HOST": "'localhost'",
                "PORT": 8080,
                "SSL_ENABLED": true,
                "THREAD_COUNT": "?[MAX_THREADS * 2]"
            },
            "LOGGING_LEVEL": "'DEBUG'",
            "EXPR": "?[MAX_THREADS + 5]"
        }'''
        output = self.run_translator(input_data)

        expected_output = '''SERVER_CONFIG(
    MAX_THREADS => 8,
    HOST => 'localhost',
    PORT => 8080,
    SSL_ENABLED => true,
    THREAD_COUNT is 16;
)
LOGGING_LEVEL is 'DEBUG';
EXPR is 13;
'''
        self.assertEqual(output, expected_output)

    def test_empty_config(self):
        input_data = '''{
            "CONFIG": {}
        }'''
        output = self.run_translator(input_data)

        expected_output = '''CONFIG(
)
'''
        self.assertEqual(output, expected_output)

    def test_invalid_expression(self):
        input_data = '''{
            "INVALID_EXPRESSION": "?[MAX_THREADS * ]"
        }'''
        with self.assertRaises(ValueError):
            self.run_translator(input_data)


if __name__ == '__main__':
    unittest.main()
