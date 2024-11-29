import os
import cmd
import tarfile
import csv
import shlex
import datetime
import getpass
import socket


class ShellEmulator(cmd.Cmd):
    def __init__(self, config_path):
        super().__init__()
        self.config = self._load_config(config_path)
        self.hostname = self.config.get("hostname", "localhost")
        self.username = getpass.getuser()
        self.fs_path = self.config["fs_path"]
        self.log_path = self.config["log_path"]
        self.startup_script = self.config.get("startup_script")  # Путь к стартовому скрипту
        self.current_dir = "/"
        self.previous_dir = "/"  # Новая переменная для хранения предыдущей директории
        self._load_virtual_fs()
        self._update_prompt()

        # Выполнение стартового скрипта, если указан и существует
        if self.startup_script and os.path.exists(self.startup_script):
            self._run_startup_script(self.startup_script)
        elif self.startup_script:
            print(f"Стартовый скрипт '{self.startup_script}' не найден.")

    def _load_config(self, config_path):
        """Загружает конфигурацию из CSV."""
        config = {}
        try:
            with open(config_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 2:
                        config[row[0].strip()] = row[1].strip()
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            exit(1)
        return config

    def _load_virtual_fs(self):
        """Загружает виртуальную файловую систему из tar-файла."""
        try:
            if not os.path.exists(self.fs_path):
                raise FileNotFoundError(f"Файл {self.fs_path} не найден.")
            self.tar = tarfile.open(self.fs_path, "r:")
        except Exception as e:
            print(f"Ошибка при загрузке файловой системы: {e}")
            exit(1)

    def _update_prompt(self):
        """Обновляет приглашение командной строки."""
        self.prompt = f"{self.username}@{self.hostname}:{self.current_dir}$ "

    def _log_action(self, command, result=""):
        """Логирует команды в CSV-файл."""
        try:
            with open(self.log_path, "a", newline="") as f:
                writer = csv.writer(f)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, command, result])
        except Exception as e:
            print(f"Ошибка записи в лог-файл: {e}")

    def _run_startup_script(self, script_path):
        """Выполняет команды из стартового скрипта."""
        try:
            with open(script_path, "r") as f:
                for line in f:
                    self.onecmd(line.strip())
        except Exception as e:
            print(f"Ошибка выполнения стартового скрипта '{script_path}': {e}")

    def do_ls(self, args):
        """Список файлов и папок."""
        path = self.current_dir.strip("/").replace("\\", "/")
        members = self.tar.getmembers()
        output = []

        if not path:
            for member in members:
                name_parts = member.name.split("/")
                if len(name_parts) == 1:
                    output.append(name_parts[0])
        else:
            for member in members:
                if member.name.startswith(path + "/"):
                    remaining = member.name[len(path) + 1 : ]
                    if remaining and "/" not in remaining:
                        output.append(remaining)

        print("\n".join(output))
        self._log_action(f"ls {args}")

    def do_cd(self, args):
        """Изменение текущей директории."""
        if not args or args == "/":
            self.previous_dir = self.current_dir  # Сохраняем текущую директорию перед переходом
            self.current_dir = "/"
        elif args == "-":
            # Переход в предыдущую директорию
            if self.previous_dir:
                self.current_dir, self.previous_dir = self.previous_dir, self.current_dir
            else:
                print("cd: нет предыдущей директории")
        else:
            # Приводим путь к нормальному виду (убираем лишние слэши)
            new_path = os.path.normpath(args).replace("\\", "/")

            # Если путь является абсолютным (начинается с '/'), то начинаем с корня
            if new_path.startswith("/"):
                self.previous_dir = self.current_dir  # Сохраняем текущую директорию перед переходом
                self.current_dir = "/" + new_path.lstrip("/")
            else:
                self.previous_dir = self.current_dir  # Сохраняем текущую директорию перед переходом
                self.current_dir = os.path.normpath(os.path.join(self.current_dir, new_path)).replace("\\", "/")

            # Проверка существования пути
            if not self._path_exists(self.current_dir):
                print(f"cd: {args}: Нет такого каталога")
                return

        self._update_prompt()
        self._log_action(f"cd {args}")

    def do_exit(self, args):
        """Выход из эмулятора."""
        self._log_action("exit")
        print("Выход из Shell.")
        return True

    def do_clear(self, args):
        """Очистка экрана."""
        os.system("cls" if os.name == "nt" else "clear")
        self._log_action("clear")

    def do_cp(self, args):
        """Копирование файла."""
        if not args:
            print("Использование: cp <источник> <назначение>")
            return

        try:
            args_list = shlex.split(args)
            if len(args_list) != 2:
                print("Использование: cp <источник> <назначение>")
                return

            src, dest = args_list
            src_path = os.path.normpath(os.path.join(self.current_dir, src)).replace("\\", "/").strip("/")
            dest_path = os.path.normpath(os.path.join(self.current_dir, dest)).replace("\\", "/").strip("/")

            try:
                # Закрыть файл перед модификацией
                self.tar.close()

                src_member = tarfile.open(self.fs_path, "r:").getmember(src_path)
                if not src_member.isfile():
                    print(f"Ошибка: {src} не является файлом")
                    return

                temp_tar_path = self.fs_path + ".temp"
                with tarfile.open(self.fs_path, "r:") as src_tar, tarfile.open(temp_tar_path, "w:") as new_tar:
                    for member in src_tar.getmembers():
                        if member.isfile():
                            with src_tar.extractfile(member) as f:
                                new_tar.addfile(member, f)
                        else:
                            new_tar.addfile(member)

                    dest_info = tarfile.TarInfo(dest_path)
                    dest_info.size = src_member.size
                    dest_info.mode = src_member.mode
                    dest_info.type = src_member.type

                    with src_tar.extractfile(src_path) as f:
                        new_tar.addfile(dest_info, f)

                os.replace(temp_tar_path, self.fs_path)
                print(f"Файл {src} успешно скопирован в {dest}")
                self._log_action(f"cp {src} {dest}")

            except KeyError:
                print(f"Ошибка: файл {src} не найден")
            finally:
                # Перезагрузить виртуальную файловую систему
                self._load_virtual_fs()

        except Exception as e:
            print(f"Ошибка при копировании: {e}")

    def _path_exists(self, path):
        """Проверка существования пути."""
        if path == "/":
            return True

        members = self.tar.getmembers()
        stripped_path = path.replace("\\", "/").strip("/")
        return any(
            m.name == stripped_path or stripped_path == os.path.dirname(m.name) or m.name.startswith(stripped_path + "/")
            for m in members
        )

    def default(self, line):
        """Обработка неизвестных команд."""
        print(f"Неизвестная команда: {line}")
        self._log_action(line, "Ошибка: неизвестная команда")


if __name__ == "__main__":
    config_path = "config.csv"
    if not os.path.exists(config_path):
        print(f"Файл конфигурации {config_path} не найден.")
        exit(1)
    ShellEmulator(config_path).cmdloop()
