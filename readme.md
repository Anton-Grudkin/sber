## 1. Basic python
### a) Singleton 
*Singleton* – шаблон проектирования, гарантирующий что у класса будет создан единственный экземпляр (и предоставляющий доступ к этому экземпляру). Реализация сводится к остлеживанию созданных экземпляров класса: новый экземпляр создаётся только при первом вызове конструктора, а при последующих вызовах предоставляется доступ к этому экземпляру. 

Стандартный пример реализации через метакласс:
```python
class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
```
Создадим теперь два класса:
```python
class Singleton(metaclass = MetaSingleton):
    def __init__(self, name):
        self.name = name
        
class Simple():
    def __init__(self, name):
        self.name = name
```

Разница между ними только в том что класс `Singleton` является экземпляром созданного метакласа `MetaSingleton`. Посмотрим как это проявляется:

```python
>>> Singleton('foo') is Singleton('bar')
True
>>> Simple('foo') is Simple('bar')
False
```
Вызов `Singleton()` реализован в метаклассе: в первый раз он передаётся с помощью `super()` в сам класс и создаёт экземпляр с полем `name == 'foo'`,  после чего этот экземпляр добавляется в словарь `_instances` метакласса (ключом, соответственно, является сам класс `Singleton`). При последующих вызовах `Singleton()` метакласс будет выдавать этот экземпляр не заходя в конструктор повторно, что и гарантирует требуемую единственность экземпляра класса с глобальной точкой доступа к этому экземпляру.

### b) Использование `with`
Кострукция `with ... as` (т.н. *менеджер контекста*) используется для более удобной реализации шаблона `try ... except ... finally`. Синатксис такой:
```python
with_stmt ::=  "with" with_item ("," with_item)* ":" suite
with_item ::=  expression ["as" target]
```
Контекстная переменная `with_item` должна иметь два метода:  `__enter__()` и `__exit__()`. При выполнении сначала вызывается метод `with_item.__enter__()` и результат его выполнения записывается в переменную указанную после `as` (таргет). Дальше выполняется код из `suite` и происходит следующее:
* если в нём генерируется исключение, то его параметры (тип, значние и traceback) передаются в метод `__exit__()`;
    * если после этого метод `__exit__()` возвращает `True`, то код исполняется дальше;
    * если возвращается `False`, то поднимается сгенерированное в `suite` исключение и исполнение завершается;
* если же `suite` завершается без исключений, то в `__exit__()` передаётся три `None`, а возвращаемое им значение игнорируется (и исполнение продлжается).

Таким образом метод `__exit__()` как бы реализует блок `finally` из конструкции `try ... except ... finally`. 

#### Пример:
Контестную переменную реализуем в виде следуещего класса:
```python
class controlled_execution:

    def __init__(self, final_value=True):
        self.__final_value = final_value

    def __enter__(self):
        print('setting thigs up')
        return 'foo'

    def __exit__(self, type, value, traceback):
        print(value)
        print('tearing things down')
        return self.__final_value
```
Теперь посмотрим как она работает:
```python
>>> with controlled_execution() as bar:
>>>     print(bar)
setting thigs up
foo
None
tearing things down
```
Сначала при исполнении выражения `with` вызвался метод `controlled_execution::__enter__()` и вернул значение `'foo'`, которое записалось в переменную `bar`; затем мы начпечатали `bar` и, так как код завершился без ошибок, в метод `controlled_execution::__exit__()` передались три `None` (мы напечатали `value`). 

Теперь сгенерируем исключение:
```python
>>> with controlled_execution() as bar:
>>>     print(bar)
>>>     _ = 1 / 0
setting thigs up
foo
division by zero
tearing things down
```
Здесь исключение `ZeroDivisionError` передаётся в `__exit__()` (что мы и видим), но так как он возращает `True`, прерывания не происходит. Если же инициализировать `controlled_execution` значением `False`, то переданное исключение будет поднято:
```python
>>> with controlled_execution(False) as bar:
>>>     print(bar)
>>>     _ = 1 / 0
setting thigs up
foo
division by zero
tearing things down
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-52-d42979eddc40> in <module>
      1 with controlled_execution(False) as bar:
      2     print(bar)
----> 3     _ = 1 / 0

ZeroDivisionError: division by zero
```
Типичный пример использования конструкции `with ... as` – открытие файлов, которое гарантирует, что при выходе из этого блока кода файл будет закрыт (это реализованно внутри метода `open::__exit__()`) независимо от результат выполнения.

### c) Генератор чисел Фибоначчи
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
        yield a
```
Пример работы:
```python
>>> print(list(fibonacci(10)))
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```
### d) Декоратор, логирующий время выполнения функции
См. пример использования в [`finder.py`](https://github.com/Anton-Grudkin/sber/blob/master/finder.py):
```python
def time_profile(fn):

    def with_time_profiling(*args, **kwargs):
        start_time = time.time()
        res = fn(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logging.info(f"Function '{fn.__name__}' was executed in {elapsed_time:.3f} s")
        return res

    return with_time_profiling
```
## 4. Python
### a) Поиск простого числа по индексу
Рализация в [`finder.py`](https://github.com/Anton-Grudkin/sber/blob/master/finder.py). Логирование времени выполнения выведено через модуль `logging` в отдельный файл лога `finder.log`.

Там используется два декоратора: `time_profile` просто логирует время выполнения функции (это решение задания *1d*). Второй, `time_profile_with_timeout`, принимает аргумент `timeout`, который задаёт время (в секундах), после которого вызов функции прерывается если она не успела завершиться до этого. Если функция успевает завершиться до таймацта, то логируется время её выполнения, если нет – то логируется warning с информацией об этом. Значение `timeout` можно передать через глобавльный параметр `-t` (функция `get_wrapped_finder` передаст этот аргумент в декоратор).

*NB*: в приведённой реализации декоратор `time_profile_with_timeout` не позволяет функции возвращать значения (из-за использования `multiprocessing.Process`; это можно сделать через [специальные](https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes) переменные). 

**Пример работы:**
```bash
$ python3 finder.py -h
usage: finder.py [-h] [-n N] [-t T]

Finds n-th prime number.

optional arguments:
  -h, --help  show this help message and exit
  -n N        prime number index
  -t T        timeout in seconds
```

```bash
$ python3 finder.py -n 1000
    1000-th prime number is 7919
```
В файле лога `finder.log` появятся две записи:
```log
2020-06-28 15:14:26,504 :: INFO - Function 'get_wrapped_finder' was executed in 0.000 s
2020-06-28 15:14:26,565 :: INFO - Function 'get_nth_prime' was executed in 0.059 s
```
Теперь увеличим индекс `-n`. Вызов
```bash
$ python3 finder.py -n 15000
```
ничего не выведет в консоль, но в логе мы увидим
```log
2020-06-28 15:33:26,742 :: INFO - Function 'get_wrapped_finder' was executed in 0.000 s
2020-06-28 15:33:31,797 :: WARNING - Execution of 'get_nth_prime' was terminated due to exceeding 5.0 s time quota
```
Увеличим таймаут:
```bash
$ python3 finder.py -n 15000 -t 10.0
    15000-th prime number is 163841
```
а в логе видим тогда
```log
2020-06-28 15:35:29,512 :: INFO - Function 'get_wrapped_finder' was executed in 0.000 s
2020-06-28 15:35:36,250 :: INFO - Function 'get_nth_prime' was executed in 6.736 s
```

### b) Рефакторинг и юнит тесты
Результат находится в директории [`legacy_test`](https://github.com/Anton-Grudkin/sber/tree/master/legacy_test). 

#### Рефакторинг
Обозрев исходный проект, замечаем, что все классы животных имеют схожую реализацию и различаются только параметрами. Поэтому имеет смысл создавать эти классы динамически, для чего предлагается функция `AnimalFactory`:
```python
AnimalFactory(
    animal_type    : str,
    initial_energy : Optional[int]  = 100,
    skills         : Optional[dict] = {'run' : 5, 'swim' : -1}
    ) -> Animal
```
Смысл первых двух аргументов очевиден. Методы типа `run()` или `swim()` мы будем тоже создавать динамически и они контролируются аргументом `skills`. Туда передаётся словарь, в котором ключ – это название действия (`str`), а значение (`int`) – изменение энергии при выполнении этого действия (`0` означает, что животное не умеет выполнять это действие).

Пример использования этой функции: 
```python
>>> Cat = AnimalFactory('Cat', 100, {'run' : 5, 'swim' : -1, 'fly' : -1})
>>> cat = Cat('Tom')
```
Создали класс котов `Cat` и кота `cat`, посмотрим как он работает:
```
>>> cat.say()
Hello, i'm Cat and my name is Tom
>>> cat.get_energy
100
>>> cat.run()
My name is Tom and i run
>>> cat.swim()
My name is Tom and i can't swim
>>> cat.get_energy
95
```
Чтобы создать классы для всех упомянутых в проекте животных, предлагается записать их параметры в JSON файл `animals.json` в таком виде:
```json
{
    "Cat": [
            100,
            {
                "fly": 0,
                "run": 5,
                "swim": 0
            }
        ]
    ...
}
```
Загрузив этот файл в словарь `animals`, создать все требуемые классы можно в две строчки:
```python
for animal, params in animals.items():
    exec(f"{animal} = AnimalFactory('{animal}', *{params})")
```
#### Тестирование
