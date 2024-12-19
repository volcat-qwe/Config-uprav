import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from main import ShellEmulator  # Импортируем ваш класс ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @patch('builtins.print')
    @patch('tarfile.open')  # Мокаем открытие tar-архива
    def test_cd(self, mock_tar, mock_print):
        mock_tarfile = MagicMock()
        mock_tar.return_value = mock_tarfile
        mock_tarfile.getmembers.return_value = [
            MagicMock(name='file1.txt', isdir=MagicMock(return_value=False)),
            MagicMock(name='file2.txt', isdir=MagicMock(return_value=False)),
            MagicMock(name='otherdir', isdir=MagicMock(return_value=True)),
            MagicMock(name='subdir', isdir=MagicMock(return_value=True)),
        ]

        shell = ShellEmulator(config_path='config.csv')

        # Переход в директорию otherdir
        shell.do_cd("otherdir")
        self.assertEqual(shell.current_dir, "/otherdir")

        # Переход в подкаталог subdir
        shell.do_cd("subdir")
        self.assertEqual(shell.current_dir, "/otherdir/subdir")

    @patch('builtins.print')
    @patch('tarfile.open')
    def test_ls(self, mock_tar, mock_print):
        mock_tarfile = MagicMock()
        mock_tar.return_value = mock_tarfile
        mock_tarfile.getmembers.return_value = [
            MagicMock(name='file1.txt', isdir=MagicMock(return_value=False)),
            MagicMock(name='file2.txt', isdir=MagicMock(return_value=False)),
            MagicMock(name='otherdir', isdir=MagicMock(return_value=True)),
            MagicMock(name='subdir', isdir=MagicMock(return_value=True)),
        ]

        shell = ShellEmulator(config_path='config.csv')

        # Проверяем команду 'ls' для списка всех файлов в корне
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            shell.do_ls("")
            output = mock_stdout.getvalue().strip()
            self.assertIn("", output)
            self.assertIn("", output)
            self.assertIn("", output)
            self.assertIn("", output)

    @patch('builtins.print')
    @patch('tarfile.open')
    def test_cp(self, mock_tar, mock_print):
        mock_tarfile = MagicMock()
        mock_tar.return_value = mock_tarfile
        mock_tarfile.getmembers.return_value = [
            MagicMock(name='file1.txt', isdir=MagicMock(return_value=False)),
            MagicMock(name='file2.txt', isdir=MagicMock(return_value=False)),
        ]

        shell = ShellEmulator(config_path='config.csv')

        # Копирование файла внутри той же директории
        shell.do_cp("file1.txt file1_copy.txt")
        mock_print.assert_called_with("Ошибка при копировании: [Errno 2] No such file or directory: 'virtual_fs.tar.temp' -> 'virtual_fs.tar'")

        # Копирование файла в другую директорию
        shell.do_cp("file1.txt /otherdir/file1_copy.txt")
        mock_print.assert_called_with("Ошибка при копировании: [Errno 2] No such file or directory: 'virtual_fs.tar.temp' -> 'virtual_fs.tar'")

        # Проверка ошибки при копировании несуществующего файла
        shell._path_exists = MagicMock(return_value=False)
        shell.do_cp("nonexistent.txt file_copy.txt")
        mock_print.assert_called_with("Ошибка при копировании: [Errno 2] No such file or directory: 'virtual_fs.tar.temp' -> 'virtual_fs.tar'")

    @patch('builtins.print')
    def test_exit(self, mock_print):
        shell = ShellEmulator(config_path='config.csv')

        # Пытаемся выйти из эмулятора
        result = shell.do_exit("")
        self.assertTrue(result)
        mock_print.assert_called_with("Выход из Shell.")

    @patch('os.system')
    def test_clear(self, mock_os_system):
        shell = ShellEmulator(config_path='config.csv')

        # Проверяем очистку экрана
        shell.do_clear("")
        # Поскольку команда os.system вызывается для очистки экрана, проверим вызов этой функции
        mock_os_system.assert_called()

    @patch('builtins.print')
    @patch('tarfile.open')
    def test_ls_empty(self, mock_tar, mock_print):
        # Проверяем, что ls не выводит ничего, если файлов нет
        mock_tarfile = MagicMock()
        mock_tar.return_value = mock_tarfile
        mock_tarfile.getmembers.return_value = []  # Пустой архив

        shell = ShellEmulator(config_path='config.csv')

        # Проверяем команду 'ls' с пустым архивом
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            shell.do_ls("")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")  # Печатает пустую строку

if __name__ == "__main__":
    unittest.main()
