## Задание 1 
```
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\begin{equation}
    \int_{x}^{\infty} \frac{dt}{t(t^2 - 1) \log t} = \int_{x}^{\infty} \frac{1}{t \log t} \left( \sum_{m} t^{-2m} \right) dt = \sum_{m} \int_{x}^{\infty} \frac{t^{-2m}}{t \log t} dt
\end{equation}

\begin{equation}
    = \sum_{m} -\int_{u}^{\infty} \frac{t^{-2m}}{\log t} dt \bigg|_{(u = t^{-2m})} = -\sum_{m} \text{li}(x^{-2m})
\end{equation}

\textbf{ФИО студента:} Иванов Иван Иванович

\end{document}
```
![image](https://github.com/user-attachments/assets/f19f64b7-637e-451f-84cd-a65112fc64f7)

## Задание 2
```
@startuml
actor "Студент Черновасиленко Д. С." as Студент
entity Piazza as Платформа
actor Преподаватель as Преподаватель

Студент -> Платформа : Поиск задач
Платформа -> Студент : Получение задачи
Студент -> Платформа : Публикация решения
Платформа -> Преподаватель : Задача опубликована
Преподаватель -> Платформа : Поиск решений
Платформа -> Преподаватель : Решение найдено
Платформа -> Студент : Решение опубликовано

Студент -> Платформа : Проверка оценки
Платформа -> Студент : Оценка получена
Студент -> Платформа : Поиск решений
Платформа -> Студент : Публикация оценки
Платформа -> Преподаватель : Оценка опубликована

@enduml
```
![image](https://github.com/user-attachments/assets/e41a2965-34fd-4a44-af90-82d7975b1d71)

## Задание 3 
Создадим файл с расширением .nw, назовем его quicksort.nw, содержащий следующий текст:
```
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}

% Title and author information
\title{Алгоритм быстрой сортировки}
\author{Черновасиленко Д.С.}
\maketitle

\section{Введение}
Быстрая сортировка - это эффективный алгоритм сортировки, использующий принцип "разделяй и властвуй".

\section{Алгоритм}
\begin{itemize}
    \item Выберите опорный элемент из массива.
    \item Разделите массив на две части - элементы меньше опорного и больше опорного.
    \item Рекурсивно примените алгоритм к подмассивам.
\end{itemize}

\section{Исходный код}
\begin{verbatim}
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
\end{verbatim}
\footnote{Разработал Черновасиленко Д.С.}

\end{document}

```
Компиляций nw-файла в pdf-файл с использованием noweb: 
```
noweb quicksort.nw
pdflatex quicksort.tex
```

Исходный код .py : 
```
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

## Задание 4

main.py
```
"""
Основной модуль приложения.
"""

from utils import add_numbers

def main():
    """Главная функция."""
    result = add_numbers(5, 10)
    print(f"Результат: {result}")

if __name__ == "__main__":
    main()
```

utils.py
```
"""
Модуль утилит.
"""

def add_numbers(a, b):
    """Сложить два числа."""
    return a + b
```
Конфигурационный файл Doxygen
```
doxygen -g Doxyfile
```
В файле Doxyfile передадим следующие параметры
```
# Выберите путь к входным файлам
INPUT = ./main.py ./utils.py

# Установите язык
PROJECT_LANGUAGES = Python

# Установите имя проекта и авторство
PROJECT_NAME = "Мой проект"
PROJECT_BRIEF = "Это пример проекта."
PROJECT_VERSION = "1.0"
GENERATE_LATEX = YES
LATEX_HEADER = Ваше_имя_Фамилия

# Включите утилиты
HAVE_DOT = YES
```
Генерируем документ
```
doxygen Doxyfile
```
```
cd docs/latex
make
```
Проверка на русские символы
```
# Кодировка документа
USE_MDFILE_AS_MAINPAGE = YES
```

# Задание 5
