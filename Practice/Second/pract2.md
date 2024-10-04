# Практическая работа 2.Черновасиленко, ИКБО-63-23

## Задание 1
Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

## Решение 

Чтобы узнать нам о служебной информации пакета воспользуемся командой apt show python3-matplotlib

```
ser1@user1-VirtualBox:~$ apt show python3-matplotlib
Package: python3-matplotlib
Version: 3.6.3-1ubuntu5
Priority: optional
Section: universe/python
Source: matplotlib
Origin: Ubuntu
```

Для установки пакета без использования pip, можно использоваться sudo apt-get install python3-matplotlib

```
ser1@user1-VirtualBox:~$ sudo apt-get install python3-matplotlib
```
или же 
```
pip install git+https://github.com/matplotlib/matplotlib.git
cd matplotlib
python setup.py install
```

## Задание 2
Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

## Решение 
Для начала установим npm для установки пакетов. 
```
ser1@user1-VirtualBox:~$ sudo install npm
```

Теперь мы можем просмотреть пакет.

```
user1@user1-VirtualBox:~$ npm view express 

express@4.21.0 | MIT | deps: 31 | versions: 279
Fast, unopinionated, minimalist web framework
http://expressjs.com/

keywords: express, framework, sinatra, web, http, rest, restful, router, app, api

dist
.tarball: https://registry.npmjs.org/express/-/express-4.21.0.tgz
.shasum: d57cb706d49623d4ac27833f1cbc466b668eb915
.integrity: sha512-VqcNGcj/Id5ZT1LZ/cfihi3ttTn+NJmkli2eZADigjq29qTlWi/hAQ43t/VLPq8+UX06FCEx3ByOYet6ZFblng==
.unpackedSize: 220.8 kB

dependencies:
accepts: ~1.3.8      etag: ~1.8.1         qs: 6.13.0           
body-parser: 1.20.3  finalhandler: 1.3.1  range-parser: ~1.2.1 
content-type: ~1.0.4 fresh: 0.5.2         safe-buffer: 5.2.1   
cookie: 0.6.0        http-errors: 2.0.0   send: 0.19.0         
debug: 2.6.9         methods: ~1.1.2      statuses: 2.0.1      
depd: 2.0.0          on-finished: 2.4.1   type-is: ~1.6.18     
encodeurl: ~2.0.0    parseurl: ~1.3.3     utils-merge: 1.0.1   
escape-html: ~1.0.3  proxy-addr: ~2.0.7   vary: ~1.1.2         
(...and 7 more.)

maintainers:
- wesleytodd <wes@wesleytodd.com>
- dougwilson <doug@somethingdoug.com>
- linusu <linus@folkdatorn.se>
- sheplu <jean.burellier@gmail.com>
- blakeembrey <hello@blakeembrey.com>
- ulisesgascon <ulisesgascondev@gmail.com>
- mikeal <mikeal.rogers@gmail.com>

dist-tags:
latest: 4.21.0  next: 5.0.0     

published 2 weeks ago by wesleytodd <wes@wesleytodd.com>
```
## Задание 3
Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.
## Решение
```
digraph G {
    // Matplotlib зависимости
    Matplotlib [label="Matplotlib", shape=box];
    Numpy [label="NumPy", shape=ellipse];
    Pillow [label="Pillow", shape=ellipse];
    Kiwisolver [label="KiwiSolver", shape=ellipse];
    Pyparsing [label="PyParsing", shape=ellipse];
    PythonDateutil [label="Python Dateutil", shape=ellipse];

    Matplotlib -> Numpy;
    Matplotlib -> Pillow;
    Matplotlib -> Kiwisolver;
    Matplotlib -> Pyparsing;
    Matplotlib -> PythonDateutil;

    // Express зависиимости
    Express [label="Express", shape=box];
    BodyParser [label="Body Parser", shape=ellipse];
    Cookie [label="Cookie", shape=ellipse];
    Debug [label="Debug", shape=ellipse];
    Finalhandler [label="Finalhandler", shape=ellipse];
    Methods [label="Methods", shape=ellipse];
    Parseurl [label="Parseurl", shape=ellipse];
    PathToRegexp [label="Path to Regexp", shape=ellipse];

    Express -> BodyParser;
    Express -> Cookie;
    Express -> Debug;
    Express -> Finalhandler;
    Express -> Methods;
    Express -> Parseurl;
    Express -> PathToRegexp;

    // Для равномерного рисунка (опционально)
    Kiwisolver -> Express [style=invis];
}
```
![Alt text](https://raw.githubusercontent.com/volcat-qwe/Config-uprav/refs/heads/main/Practice/First/graphs.svg)
## Задание 4

Следующие задачи можно решать с помощью инструментов на выбор:

Решатель задачи удовлетворения ограничениям (MiniZinc). SAT-решатель (MiniSAT). SMT-решатель (Z3). Изучить основы программирования в ограничениях. Установить MiniZinc, разобраться с основами его синтаксиса и работы в IDE.

Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте all_different). Найти минимальное решение для суммы 3 цифр.


## Решение

```
include "globals.mzn";

array[1..6] of var 0..9: digits;
constraint all_different(digits);

var int: sum_first = sum(digits[1..3]);
var int: sum_last = sum(digits[4..6]);

constraint sum_first = sum_last;
solve minimize sum_first;
```


На выводе получаем: 
```
digits = [8, 1, 0, 4, 3, 2];
_objective = 9;
----------
digits = [6, 2, 0, 4, 3, 1];
_objective = 8;
----------
==========
Finished in 283msec.
```







## Задание 5

Решить на MiniZinc задачу о зависимостях пакетов для рисунка, приведенного ниже.

![alt text](https://raw.githubusercontent.com/true-grue/kisscm/blob/847fc05a9ef7131fd5e71a110aae510ecdd5ce37/pract/images/pubgrub.png)

## Решение
```
set of int: MenuVersion = {100, 110, 120, 130, 150};
set of int: DropdownVersion = {230, 220, 210, 200, 180};
set of int: IconsVersion = {100, 200};

var MenuVersion: menu;
var DropdownVersion: dropdown;
var IconsVersion: icons;

constraint if menu >= 110 then dropdown >= 200 else dropdown = 180 endif;

constraint if dropdown <= 200 /\ dropdown > 180 then icons = 200 else icons = 100 endif;

solve satisfy;
```

На выводе : 
```
menu = 100;
dropdown = 180;
icons = 100;
----------
Finished in 110msec.
```
