import unittest
from unittest.mock import patch, MagicMock
from visualizer import get_dependencies, create_graph
from graphviz import Digraph


class TestDependencyGraph(unittest.TestCase):
    @patch('subprocess.run')
    def test_get_dependencies(self, mock_subprocess_run):
        """
        Тестирует функцию get_dependencies для корректного построения зависимостей.
        """
        # Настраиваем mock для команды apt-cache depends
        mock_subprocess_run.side_effect = [
            MagicMock(stdout="Depends: libexample1\nDepends: libexample2\n", returncode=0),  # Для testpkg
            MagicMock(stdout="Depends: libexample2\n", returncode=0),  # Для libexample1
            MagicMock(stdout="", returncode=0)  # Для libexample2
        ]

        package_name = "testpkg"
        depth = 2
        repo_url = "http://example.com"

        # Ожидаемый результат
        expected_dependencies = {
            "testpkg": ["libexample1", "libexample2"],
            "libexample1": ["libexample2"],
            "libexample2": []
        }

        # Выполнение функции
        result = get_dependencies(package_name, depth, repo_url)

        # Проверка результата
        self.assertEqual(result, expected_dependencies)

    @patch('subprocess.run')
    def test_get_dependencies_with_error(self, mock_subprocess_run):
        """
        Тестирует функцию get_dependencies для обработки ошибок.
        """
        # Настраиваем mock для команды apt-cache depends, чтобы вызывать ошибку
        mock_subprocess_run.return_value = MagicMock(stdout="", stderr="Package not found", returncode=1)

        package_name = "nonexistentpkg"
        depth = 1
        repo_url = "http://example.com"

        # Ожидаемый результат
        expected_dependencies = {
            "nonexistentpkg": []
        }

        # Выполнение функции
        result = get_dependencies(package_name, depth, repo_url)

        # Проверка результата
        self.assertEqual(result, expected_dependencies)

    def test_create_graph(self):
        """
        Тестирует функцию create_graph для корректного построения графа.
        """
        # Входные данные: зависимости
        dependencies = {
            "testpkg": ["libexample1", "libexample2"],
            "libexample1": ["libexample2"],
            "libexample2": []
        }

        # Создание графа
        graph = create_graph(dependencies)

        # Проверка типа
        self.assertIsInstance(graph, Digraph)

        # Проверяем, что граф содержит корректные рёбра
        expected_edges = [
            "testpkg -> libexample1",
            "testpkg -> libexample2",
            "libexample1 -> libexample2",
        ]
        # Сравниваем строки из DOT-формата
        for edge in expected_edges:
            self.assertIn(edge, graph.source)

    def test_create_graph_empty(self):
        """
        Тестирует функцию create_graph с пустыми зависимостями.
        """
        # Входные данные: пустые зависимости
        dependencies = {}

        # Создание графа
        graph = create_graph(dependencies)

        # Проверка типа
        self.assertIsInstance(graph, Digraph)

        # Проверка, что граф пустой (нет рёбер)
        self.assertNotIn("->", graph.source)


if __name__ == "__main__":
    unittest.main()
