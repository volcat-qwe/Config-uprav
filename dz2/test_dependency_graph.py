import unittest
from graphviz import Digraph

# Импортируем тестируемые функции
# from ваш_скрипт import mock_get_dependencies, get_dependencies, create_graph

def mock_get_dependencies(package_name):
    """Имитация получения зависимостей (для тестов)."""
    mock_dependencies = {
        "packageA": ["packageB", "packageC"],
        "packageB": ["packageD"],
        "packageC": [],
        "packageD": ["packageE"],
        "packageE": []
    }
    return mock_dependencies.get(package_name, [])

def get_dependencies(package_name, depth):
    """Получение зависимостей пакета с учётом глубины."""
    dependencies = {}
    queue = [(package_name, 0)]
    visited = set()

    while queue:
        pkg, level = queue.pop(0)

        if pkg in visited or level >= depth:
            continue

        visited.add(pkg)
        deps = mock_get_dependencies(pkg)
        dependencies[pkg] = deps
        queue.extend((dep, level + 1) for dep in deps)

    return dependencies

def create_graph(dependencies):
    """Создание графа зависимостей в формате Graphviz."""
    dot = Digraph(format='png')
    for pkg, deps in dependencies.items():
        for dep in deps:
            dot.edge(pkg, dep)
    return dot


class TestDependencyFunctions(unittest.TestCase):

    def test_mock_get_dependencies(self):
        """Тестирование mock_get_dependencies."""
        self.assertEqual(mock_get_dependencies("packageA"), ["packageB", "packageC"])
        self.assertEqual(mock_get_dependencies("packageB"), ["packageD"])
        self.assertEqual(mock_get_dependencies("packageC"), [])
        self.assertEqual(mock_get_dependencies("nonexistent"), [])

    def test_get_dependencies(self):
        """Тестирование get_dependencies."""
        expected = {
            "packageA": ["packageB", "packageC"],
            "packageB": ["packageD"],
            "packageD": ["packageE"],
            "packageC": []
        }
        result = get_dependencies("packageA", 3)
        self.assertEqual(result, expected)

        # Проверка глубины
        result_depth_1 = get_dependencies("packageA", 1)
        expected_depth_1 = {
            "packageA": ["packageB", "packageC"],
        }
        self.assertEqual(result_depth_1, expected_depth_1)

    def test_create_graph(self):
        """Тестирование create_graph."""
        dependencies = {
            "packageA": ["packageB", "packageC"],
            "packageB": ["packageD"],
            "packageD": ["packageE"],
        }
        
        graph = create_graph(dependencies)

        # Проверка рёбер в графе
        edges = ['packageA -> packageB', 'packageA -> packageC', 'packageB -> packageD', 'packageD -> packageE']
        for edge in edges:
            self.assertIn(edge, "".join(graph.body))

if __name__ == "__main__":
    unittest.main()
