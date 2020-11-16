# Домашнее задание 3 к лекции 10

Склонировать репозиторий и перейти в директорию:
```
  git clone https://github.com/Mstrutov/techno_minimum_hw/
  cd techno_minimum_hw/hw_10/p3_new
```

У make есть следующие цели:
- `make healthcheck` - проверяет, установлен ли docker и docker-compose
- `make dependencies` - устанавливает docker
- `make build` - собирает образы файлового сервера, redis и mongo
- `make start` - запускает в фоне контейнеры с сервером, redis и mongo в сети host, монтируя `/var/log/` для доступа к логам сервера. Сервер слушает порт 8080.
- `make stop` - останавливает контейнеры.
- `make clean` - удаляет сгенерированные образы и `/var/log/server.log`.

Предполается такое использование сервера:
1. `make healthcheck` - если docker или docker-compose не установлены, `make dependencies`
2. `make build`
3. `make start`
4. Ручное тестирование сервера
5. `make stop`
6. `cat /var/log/server.log`
6. `make clean`

Команды для тестирования:
- Записать/перезаписать файл: `curl --request PUT --header "Content-Type: application/json" --data '{"username":"xyz", "password":"abc"}' http://localhost:8080/storage/my-file`
- Удалить файл: `curl  --request DELETE --verbose http://localhost:8080/storage/my-file`
- Получить содержимое файла: `curl  --request GET --verbose http://localhost:8080/storage/my-file`
