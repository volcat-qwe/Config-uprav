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

