## Задание 1
На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.
![image](https://github.com/user-attachments/assets/7334ae1e-6ec0-43b5-96b1-8d11f31134d2)

![image](https://github.com/user-attachments/assets/1107f249-8cf0-4d62-b463-d92b01244880)
## Задание 2
Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.
![image](https://github.com/user-attachments/assets/df5bca0e-1d6e-4535-9c63-1e861de31a69)
В prog.py запишем: 
![image](https://github.com/user-attachments/assets/d16b5e3d-9eb6-4447-a314-9bf03b7ac20f)
## Задание 3
Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

```
# Инициализация первого репозитория и настройка
git init
git config user.name "volcat1"
git config user.email "volcat1@example.com"
echo 'print("Hi ConfigUprav!")' > prog.py
git add prog.py
git commit -m "first commit"

# Создание bare-репозитория
mkdir -p repository
cd repository
git init --bare server

# Возвращение в основной репозиторий, подключение к серверу и пуш
cd -
git remote add server repository/server
git remote -v
git push server master

# Клонирование серверного репозитория в клиентский
git clone repository/server repository/client
cd repository/client
git config user.name "volcat2"
git config user.email "volca2@gmail.com"

# Добавление нового файла и коммит
echo "author info:" > readme.md
git add readme.md
git commit -m "docs"

# Переименование удаленного репозитория и пуш
git remote rename origin server
git push server master

# Возвращение в основной репозиторий, чтобы сделать pull
cd ../repository
git pull server master --no-rebase  # Используем merge вместо rebase

# Внесение изменений от coder1 и пуш
echo "Author: volcat1" >> readme.md
git add readme.md
git commit -m "volcat1 info"
git push server master

# Переход в клиентский репозиторий и внесение изменений от coder2
cd client
echo "Author: volcat2" >> readme.md
git add readme.md
git commit -m "volcat2 info"

# Перед `push` выполняем `pull` с merge, чтобы избежать линейной истории
git pull server master --no-rebase
git push server master

# Получение последних изменений с сервера
git pull server master --no-rebase

# Последний коммит и пуш исправлений в readme
git add readme.md
git commit -m "readme fix"
git push server master

# Переход к bare-репозиторию и просмотр истории
cd ..
cd server
git log -n 5 --graph --decorate --all
```

![image](https://github.com/user-attachments/assets/c89cf3db-907a-491a-9252-1cf175506407)


## Задание 4
Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.
```
import os
import subprocess

def find_git_root(path):
    """Finds the root of the git repository containing the given path."""
    while path != os.path.dirname(path):
        if os.path.isdir(os.path.join(path, '.git')):
            return path
        path = os.path.dirname(path)
    return None

def main():
    # Ищем корень git
    current_dir = os.getcwd()
    git_root = find_git_root(current_dir)
    if git_root is None:
        print('Not inside a git repository')
        return

    git_objects_dir = os.path.join(git_root, '.git', 'objects')

    # Список для хранения идентификаторов объектов
    object_ids = []

    # Пройдемся по каталогу .git/objects
    for root, dirs, files in os.walk(git_objects_dir):
        # Skip 'info' and 'pack' directories
        dirs[:] = [d for d in dirs if d not in ('info', 'pack')]

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            for filename in os.listdir(dir_path):
                # Construct object ID
                object_id = dir_name + filename
                object_ids.append(object_id)

    # Удалим копии
    object_ids = list(set(object_ids))

    # For each object ID, run "git cat-file -p <object_id>"
    for object_id in object_ids:
        try:
            output = subprocess.check_output(['git', 'cat-file', '-p', object_id], stderr=subprocess.STDOUT, cwd=git_root)
            print('Object ID:', object_id)
            print(output.decode('utf-8', errors='replace'))
            print('-' * 40)
        except subprocess.CalledProcessError as e:
            print('Error processing object ID:', object_id)
            print(e.output.decode('utf-8', errors='replace'))
            print('-' * 40)

if __name__ == '__main__':
    main()
```
