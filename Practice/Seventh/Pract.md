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

