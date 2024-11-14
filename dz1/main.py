import csv
import os
import shutil
import tarfile
from datetime import datetime

# Глобальные переменные
ROOT_DIR = None
previous_directory = None  # Хранит предыдущую директорию
LOG_FILE = None  # Имя лог-файла, инициализируем позже.
STARTUP_SCRIPT = None  # Путь к стартовому скрипту
TEST_DIRECTORY = None  # Директория для тестов


def load_config(filename='config.csv'):
    """Загрузка конфигурации из CSV файла."""
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            config = next(reader)  # считываем первую строку как словарь
            return config
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        return {}
    except StopIteration:
        print("Ошибка: файл конфигурации пуст.")
        return {}


def log_action(action):
    """Записывает действие в лог-файл с текущей датой и временем."""
    if LOG_FILE:  # Проверяем, что имя лог-файла задано
        with open(LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action])


def execute_commands_from_file(filename):
    """Выполняет команды из указанного файла."""
    try:
        if not os.path.isfile(filename):
            print(f"Ошибка: '{filename}' не является файлом.")
            log_action(f"Ошибка: '{filename}' не является файлом.")
            return

        with open(filename, 'r') as file:
            for line in file:
                command = line.strip()
                if command:  # Если строка не пустая
                    print(f"Выполнение команды: {command}")
                    exec_command(command)
    except PermissionError:
        print(f"Ошибка: Доступ запрещен к файлу '{filename}'.")
        log_action(f"Ошибка: Доступ запрещен к файлу '{filename}'.")
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        log_action(f"Ошибка: файл '{filename}' не найден.")
    except Exception as e:
        print(f"Ошибка при выполнении команд из файла: {e}")
        log_action(f"Ошибка при выполнении команд из файла: {e}")


def exec_command(command):
    """Выполняет команду пользователя."""
    if command.startswith('cd '):
        path = command.split(' ', 1)[1]
        cd(path)
    elif command.strip() == 'ls':
        ls()
    elif command.startswith('cp '):
        parts = command.split(' ', 2)
        if len(parts) == 3:
            cp(parts[1], parts[2])
    elif command.startswith('test '):
        test_file = command.split(' ', 1)[1]  # Получаем имя тестового файла
        full_test_file_path = os.path.join(TEST_DIRECTORY, test_file)

        if not os.path.isfile(full_test_file_path):
            print(f"Ошибка: файл теста '{full_test_file_path}' не найден.")
            log_action(f"Ошибка: файл теста '{full_test_file_path}' не найден.")
            return

        execute_commands_from_file(full_test_file_path)
    elif command.startswith('extract '):
        parts = command.split(' ', 1)
        if len(parts) == 2:
            extract_tar(parts[1])  # Извлечение в текущую директорию
    elif command.strip() == 'clear':
        clear()
    else:
        print(f"Ошибка: Команда '{command}' не существует.")
        log_action(f"Ошибка: Команда '{command}' не существует.")


def ls(path='.'):
    """Вывод названий файлов в указанной директории."""
    try:
        files = os.listdir(path)
        for file in files:
            print(file)
        log_action(f"ls выполнен в {path}")
    except FileNotFoundError:
        print(f"Ошибка: Директория '{path}' не найдена.")
        log_action(f"Ошибка: Директория '{path}' не найдена.")
    except PermissionError:
        print(f"Ошибка: Нет доступа к директории '{path}'.")
        log_action(f"Ошибка: Нет доступа к директории '{path}'.")


def cp(source, destination):
    """Копирование файла из источника в назначение."""
    try:
        full_source = os.path.join(ROOT_DIR, source)
        full_destination = os.path.join(ROOT_DIR, destination)

        shutil.copy2(full_source, full_destination)
        print(f"Файл '{source}' успешно скопирован в '{destination}'.")
        log_action(f"Копирование: '{source}' -> '{destination}'")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{source}' не найден.")
        log_action(f"Ошибка: Файл '{source}' не найден.")
    except PermissionError:
        print(f"Ошибка: Нет доступа к '{destination}'.")
        log_action(f"Ошибка: Нет доступа к '{destination}'.")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        log_action(f"Ошибка при копировании: {e}")


def extract_tar(archive_path, extract_path=None):
    """Извлекает содержимое TAR архива в указанной директории."""
    if extract_path is None:
        extract_path = ROOT_DIR;  # Используем текущую директорию по умолчанию

    try:
        with tarfile.open(archive_path, 'r') as tar:
            tar.extractall(path=extract_path)  # Извлекаем все содержимое
        print(f"Архив '{archive_path}' успешно извлечен в '{extract_path}'.")
        log_action(f"Извлечение: '{archive_path}' в '{extract_path}'")
    except FileNotFoundError:
        print(f"Ошибка: Архив '{archive_path}' не найден.")
        log_action(f"Ошибка: Архив '{archive_path}' не найден.")
    except tarfile.TarError:
        print(f"Ошибка: Не удалось извлечь архив '{archive_path}'.")
        log_action(f"Ошибка: Не удалось извлечь архив '{archive_path}'.")


def cd(path):
    """Изменение текущей рабочей директории."""
    global previous_directory
    current_directory = os.getcwd()  # Получаем текущую директорию
    new_directory = os.path.join(current_directory, path)

    if path == '-':
        if previous_directory:
            new_directory = previous_directory
        else:
            print("Ошибка: Нет предыдущей директории для возврата.")
            return
    elif path == '..':
        print("Ошибка: Вы не можете выйти за пределы директории 'restricted_directory'.")
        return
    elif not os.path.isabs(path):  # Если путь не абсолютный, создаем его по отношению к ROOT_DIR
        new_directory = os.path.join(current_directory, path)

    # Проверяем, что новая директория находится в пределах ROOT_DIR
    if os.path.isdir(new_directory) and os.path.commonpath([new_directory, ROOT_DIR]) == ROOT_DIR:
        previous_directory = current_directory  # Обновляем предыдущую директорию
        os.chdir(new_directory)
        print(f"Текущая директория изменена на '{os.getcwd().replace(ROOT_DIR, '')}'.")
        log_action(f"cd выполнен: '{new_directory}'")
    else:
        print(f"Ошибка: '{new_directory}' не является директорией или находится вне разрешенного пути.")
        log_action(f"Ошибка: '{new_directory}' не является директорией или находится вне разрешенного пути.")


def clear():
    """Очистка экрана терминала."""
    os.system('cls' if os.name == 'nt' else 'clear')
    log_action("Очистка экрана терминала")


def terminal():
    global ROOT_DIR, LOG_FILE, STARTUP_SCRIPT, TEST_DIRECTORY
    ROOT_DIR = os.path.abspath('restricted_directory')  # Устанавливаем ROOT_DIR

    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.csv')
    config = load_config(config_path)

    # Извлекаем пути к лог-файлу, стартовому скрипту и тестовой директории
    LOG_FILE = os.path.join(os.path.abspath('..'),
                            config.get('log_file', 'session_log.csv'))  # Лог файл на уровень выше
    STARTUP_SCRIPT = os.path.join(os.path.abspath('..'),
                                  config.get('startup_script', ''))  # Стартовый скрипт на уровень выше
    TEST_DIRECTORY = os.path.join(os.path.abspath('..'),
                                  config.get('test_directory', 'tests'))  # Директория тестов на уровень выше

    os.chdir(ROOT_DIR)  # Переход в директорию, указанную в конфигурации

    username = config.get('username', 'guest')  # Имя компьютера из конфигурации, по умолчанию 'guest'

    log_action("Начало сеанса терминала")

    # Выполнение стартового скрипта, если он указан
    if STARTUP_SCRIPT and os.path.isfile(STARTUP_SCRIPT):
        execute_commands_from_file(STARTUP_SCRIPT)

    while True:
        cwd = os.getcwd().replace(ROOT_DIR, '')  # Убираем только ROOT_DIR из пути
        prompt = f"{username}@{username}:restricted_directory{cwd} $ "

        command = input(prompt).strip()

        if command.lower() in ['exit', 'quit']:
            print("Выход из терминала.")
            log_action("Выход из терминала")
            break
        elif command == '':
            continue
        else:
            exec_command(command)


if __name__ == "__main__":
    terminal()
