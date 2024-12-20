import argparse
import os
from graphviz import Digraph

# Имитация получения зависимостей
def mock_get_dependencies(package_name):
    # Пример зависимостей, которые могли бы быть получены из репозитория
    mock_dependencies = {
        "packageA": ["packageB", "packageC"],
        "packageB": ["packageD"],
        "packageC": [],
        "packageD": ["packageE"],
        "packageE": []
    }
    return mock_dependencies.get(package_name, [])

def get_dependencies(package_name, depth):
    """
    Получение зависимостей пакета с учетом указанной глубины.
    """
    dependencies = {}
    queue = [(package_name, 0)]
    visited = set()

    while queue:
        pkg, level = queue.pop(0)

        if pkg in visited or level >= depth:
            continue

        visited.add(pkg)

        # Имитация получения зависимостей вместо вызова subprocess
        deps = mock_get_dependencies(pkg)
        dependencies[pkg] = deps

        queue.extend((dep, level + 1) for dep in deps)

    return dependencies

def create_graph(dependencies):
    """
    Создание графа зависимостей в формате Graphviz.
    """
    dot = Digraph(format='png')
    for pkg, deps in dependencies.items():
        for dep in deps:
            dot.edge(pkg, dep)
    return dot

def main():
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей пакета.")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета.")
    parser.add_argument("--output", required=True, help="Путь к файлу для сохранения графа.")
    parser.add_argument("--depth", type=int, default=3, help="Максимальная глубина анализа зависимостей.")
    args = parser.parse_args()

    # Получение зависимостей
    dependencies = get_dependencies(args.package, args.depth)

    # Создание графа
    graph = create_graph(dependencies)

    # Сохранение графа
    output_path = args.output
    graph.render(output_path, cleanup=True)

    print(f"Граф зависимостей успешно сохранен в {output_path}.png")

if __name__ == "__main__":
    main()
