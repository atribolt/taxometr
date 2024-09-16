# Taxometr - утилита для ведения журнала трудозатрат

- [Функцинал](#функционал)
- [В разработке](#планируется-сделать)
- [Консольное управление](#cli)
- [Установка](#установка)


### Функционал
- хранение трудозатрад в БД sqlite или Postgre
- CLI
  - создание групп задач
  - создание задач
  - запуск задачи
  - просмотр информации о задаче
    - время затраченное за сегодня
    - время затраченное за месяц
    - общее затраченное время

### Планируется сделать
- [ ] HTTP api для удаленного управления
- [ ] небольшая WEB страничка, для удобного визуального управления
- [ ] экспорт данных в таблицы
  - [ ] CSV
  - [ ] ODT


# CLI

По всем командам работет опция `--help`. 
```shell
taxometr --help
taxometr task --help
taxometr action --help
taxometr action show --help
```

Схема работы с программой:
- Создать группу задач
  ```shell
  taxometr task new 'Огород'
  
  # 1: Огород
  ```
- Создать задачу
  ```shell
  # флаг '-s' сразу запускает задачу
  taxometr action new -t 1 'Вскопать землю' -s
  # 1: (Огород) Вскопать землю
  
  taxometr action new -t 1 'Посадить морковь'
  # 2: (Огород) Посадить морковь
  
  taxometr action new -t 1  'Посадить картофель'
  # 3: (Огород) Посадить картофель
  ```
- Посмотреть список задач
  ```shell
  # По умолчанию отображаются только задачи активные сегодня
  taxometr action list
  #   id  task    action          total time      active
  # ----  ------  --------------  --------------  --------
  #    1  Огород  Вскопать землю  0:00:38         True
  
  # Посмотреть все задачи 
  taxometr action list -a
  #   id  task    action              total time      active
  # ----  ------  ------------------  --------------  --------
  #    1  Огород  Вскопать землю      0:00:41         True
  #    2  Огород  Посадить морковь    0:00:00         False
  #    3  Огород  Посадить картофель  0:00:00         False
  ```
- Запустить другую задачу
  ```shell
  taxometr action start 2
  
  # Теперь за сегодня было две задачи (активна вторая)
  taxometr action list
  #   id  task    action            total time      active
  # ----  ------  ----------------  --------------  --------
  #    1  Огород  Вскопать землю    0:12:02         False
  #    2  Огород  Посадить морковь  0:00:32         True
  ```
- Остановить активную задачу
  ```shell
  taxometr action stop
  
  # Теперь за сегодня было две задачи (все остановлены)
  taxometr action list
  #   id  task    action            total time      active
  # ----  ------  ----------------  --------------  --------
  #    1  Огород  Вскопать землю    0:12:02         False
  #    2  Огород  Посадить морковь  0:02:14         False
  ```

### Вывод информации о задаче
```shell
taxometr action show 2
```

```text
Id: 2
Task:
  Id: 1
  Title: Огород
Description: Посадить морковь
This month time: 0:02:14.628854
Today time: 0:02:14.628854
Time ranges (today):
  0:02:14 | 0.04h | 11:33:36 - 11:35:50
```


# Установка

- Установите pip
```shell
# Ubuntu >= 22.04 
sudo apt install python3-pip
pip3 install --user git+https://github.com/atribolt/taxometr.git 'taxometr[cli]'

# Arch
sudo pacman -S python-pip
pip install --user git+https://github.com/atribolt/taxometr.git 'taxometr[cli]'
```
- Проверьте правильность установки
```shell
taxometr --help
```

```
Usage: taxometr [OPTIONS] COMMAND [ARGS]...

  CLI for taxometr

Options:
  -v, --verbose  Enable verbose output (-v, -vv, -vvv)
  -c, --colored  Enable colored output
  --help         Show this message and exit.

Commands:
  action  Actions managing
  task    Task group managing
```