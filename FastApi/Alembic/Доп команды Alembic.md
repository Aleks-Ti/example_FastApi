# Полезные команды
Посмотреть историю
```bash
alembic history
```
Можно вывести в более подробном виде с флагом --verbose

```bash
alembic history --verbose
or
alembic history -v
```
Посмотреть последнюю применённую миграцию можно при помощи команды `current`. Выполните её:
```bash
alembic current
```
При просмотре истории миграций можно вывести метку актуальной миграции: для этого надо указать ключ `-i` (или `--indicate-current` в полной форме):
```bash
alembic history -i
```
Миграциям можно задавать фиксированные Revision ID прямо в команде создания миграции; если их нумеровать по порядку, например, 01, 02, 03 — файлы в директории будут хронологически упорядочены.

Фиксированный Revision ID указывается в команде `revision` при помощи ключа `--rev-id`:
```bash
(venv) ...$ alembic revision --autogenerate -m "Initial structure" --rev-id 01
# Какие-то изменения в моделях.
(venv) ...$ alembic revision --autogenerate -m "Add new models" --rev-id 02
```
При желании можно добавить к названию файлов с миграциями дату и время их создания, поменяв в файле _alembic.ini_ значение по умолчанию; изначально в файле строка с переменной может быть закомментирована.
```bash
# Заменяем строку
file_template = %%(rev)s_%%(slug)s
# на такую:
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```
Теперь имена файлов миграций будут выглядеть так:
```bash
2022_02_28_1235-e6bd2f1ce032_add_description_to_meetingroom.py
```
Шаблоны имён можно комбинировать как угодно, например, можно задать и такой шаблон:
```bash
file_template = %%(rev)s-%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(slug)s
```
Если теперь выполнить команду с указанием собственного Revision ID...
```bash
(venv) ...$ alembic revision -m "Initial structure" --rev-id 01
```
...то имя файла получится таким:
```bash
01-2022_02_28_1235-initial_structure.py
```