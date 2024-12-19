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
python3 visualizer.py --graphviz-path usr/bin/ --package curl --output curl.
png --depth 2 --repo-url http://archive.ubuntu.com/
```
На выходе получаем ![curl png](https://github.com/user-attachments/assets/e9ba4e3d-9867-48fb-8c6b-a55827b9b94a)

# Запуск тестов
```
python3 -m unittest test_dependency_graph.py
```
