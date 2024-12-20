# Клонирование репозитория для запуска программы

```
git clone https://github.com/volcat-qwe/Config-uprav.git
cd Config-uprav
cd dz2
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
# Установка graphviz
```
sudo apt install graphviz
```

# Запуск эмулятора
-h - флаг-помощник программы
```
python3 vizualizer.py -h #просмотр необходимых флагов для запуска программы 
```
Пример использования программы
```
python3 dependencies.py --package pa
ckageA --output qwe  --depth 3
```
На выходе получаем ![qwe](https://github.com/user-attachments/assets/8169eb6b-53ad-46e1-95a7-22f3156dc486)


# Запуск тестов
```
python3 -m unittest test_dependency_graph.py
```
