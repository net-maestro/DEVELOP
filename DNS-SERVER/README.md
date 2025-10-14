# DNS-DOCKER-STUB

# Обновление заблокированных доменов

## Ссылка для обновления списка заблокированных доменов
Для получения актуального списка заблокированных доменов используйте следующую ссылку:
uablacklist.net/domains.txt
[Скачать список доменов](https://uablacklist.net/domains.txt)

---

## Скрипт обновления заблокированных доменов
Для обновления списка выполните скрипт:  
```bash
./update_blacklist.sh
```

 ## Обновление корневых доменов 
   curl -o root.hints https://www.internic.net/domain/named.root

   
# Полезные команды Docker
- **Остановка и удаление контейнеров:**  
  ```bash
  docker compose down
  docker rmi idcontainer
  docker compose build
  docker compose up -d
  docker exec unbound nslookup 193.176.2.1 127.0.0.1:5301
  ```
