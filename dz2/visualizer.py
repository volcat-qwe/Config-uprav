import subprocess
import argparse
import os
from graphviz import Digraph


def get_dependencies(package_name, depth, repo_url):
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
        try:
            result = subprocess.run(
                ["apt-cache", "depends", pkg],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout
            deps = []
            for line in output.splitlines():
                if line.strip().startswith("Depends:"):
                    dep = line.split(":")[1].strip()
                    if dep not in visited:  # Добавляем только те, которые ещё не обработаны
                        deps.append(dep)
            dependencies[pkg] = deps  # Добавляем зависимости только для текущего пакета
            queue.extend((dep, level + 1) for dep in deps)
        except Exception as e:
            print(f"Ошибка при обработке пакета {pkg}: {e}")
            continue
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
    parser = argparse.ArgumentParser(description="Визуализация графа зависимостей Ubuntu пакета.")
    parser.add_argument("--graphviz-path", required=True, help="Путь к программе Graphviz.")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета.")
    parser.add_argument("--output", required=True, help="Путь к файлу для сохранения графа.")
    parser.add_argument("--depth", type=int, default=3, help="Максимальная глубина анализа зависимостей.")
    parser.add_argument("--repo-url", required=True, help="URL-адрес репозитория.")

    args = parser.parse_args()

    # Установим PATH, добавляя путь к Graphviz
    os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + args.graphviz_path

    # Получение зависимостей
    dependencies = get_dependencies(args.package, args.depth, args.repo_url)

    # Создание графа
    graph = create_graph(dependencies)

    # Сохранение графа
    output_path = args.output
    graph.render(output_path, cleanup=True)

    print(f"Граф зависимостей успешно сохранен в {output_path}.png")


if __name__ == "__main__":
    main()
