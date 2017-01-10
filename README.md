# logstat.py
Скрипт считает количество строк, которые соответствуют регулярному выражению, при этом читая только новые строки в файле, т.е. не перечитывая файл с нуля.  

## Требования
`python2`

## Usage
```bash
./logstat.py /path/to/logfile.log REGEX [/path/to/stat_file.json]
```
Путь к файлу состояний является опциональным, если он не указан, то будет использован путь `/home/zabbix/scripts/log_state.json`


## Описание работы на примере
```bash
# Запускаем впервые:
$ ./logstat.py /var/log/foo.log 'Fatal error'
10
# Предположим, что /var/log/foo.log не изменился и не ротировался. Запустим ещё раз:
$ ./logstat.py /var/log/foo.log 'Fatal error'
0
# А вот теперь в файле foo.log появятся две строки с Fatal error
$ ./logstat.py /var/log/foo.log 'Fatal error'
2
```
При первом запуске скрипта на файл `/var/log/foobar.log` с регэкспом `Fatal error` скрипт будет прочтён с самой первой строки.  
При втором запуске скрипт проверит, был ли изменён файл:  
Если в файл были дописаны строки, то будут прочитаны только новые строки.  
Если файл был ротирован, то файл будет прочитан сначала.  
При этом если запустить скрипт на тот же файл, но с другим регэкспом впервые, то чтение также будет происходить с начала файла, что позволяет мониторить один и тот же файл по нескольким регэкспам.

# slack.py
Грязненький скрипт для отправки уведомлений из заббикса в Slack через хук. Требует установленного curl.

## Требования:
`curl`

## Usage
```bash
./slack.py "@username" "Zabbix subject" "Zabbix message"
```

## Установка и настройка:

* Скопировать файл slack.py в `/usr/lib/zabbix/alertscripts`
* Вставить ваш Hook URL и имя пользователя в соответствующие переменные в начале файла
* `chown zabbix:zabbix /usr/lib/zabbix/alertscripts/slack.py`
* `chmod u+x /usr/lib/zabbix/alertscripts/slack.py`
* Создать Media type в заббиксе, указав ему на этот скрипт.

### Внимание!
Для правильной работы скрипта формат сообщений в заббиксе следует настроить так:
**Subject:** `{TRIGGER.STATUS} {TRIGGER.NAME}`
**Message:**
```
HOST_NAME1={HOST.NAME1}
TRIGGER_NAME={TRIGGER.NAME}
TRIGGER_URL={TRIGGER.URL}
TRIGGER_VALUE={TRIGGER.VALUE}
TRIGGER_DESCRIPTION={TRIGGER.DESCRIPTION}
TRIGGER_SEVERITY={TRIGGER.SEVERITY}
ITEM_NAME1={ITEM.NAME1}
ITEM_NAME2={ITEM.NAME2}
ITEM_NAME3={ITEM.NAME3}
ITEM_VALUE1={ITEM.VALUE1}
ITEM_VALUE2={ITEM.VALUE2}
ITEM_VALUE3={ITEM.VALUE3}
EVENT_RECOVERY_TIME={EVENT.RECOVERY.TIME}
EVENT_RECOVERY_DATE={EVENT.RECOVERY.DATE}
EVENT_TIME={EVENT.TIME}
EVENT_DATE={EVENT.DATE}
INVENTORY_URL_A1={INVENTORY.URL.A1}
```