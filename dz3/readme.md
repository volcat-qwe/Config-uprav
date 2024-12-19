# Клонирование репозитория для запуска программы

```
git clone https://github.com/volcat-qwe/Config-uprav.git
cd Config-uprav
cd dz3
```

# Установка зависимостей
```
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```

# Установка и запуск wsl
```
wsl --install
wsl
```

# Запуск программы
-h - флаг-помощник программы
```
python3 translator -h
```
Пример запуска программы
```
python3 translator.py import.json output.json
```
# Запуск тестов
```
python3 -m unittest test_translator.py
```
