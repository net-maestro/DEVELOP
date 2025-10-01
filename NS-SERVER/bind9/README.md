---

##
- Авторитативный DNS-сервер для домена `example.local` (вы сможете заменить на свой).
- Прямая зона + одна PTR-зона.
- Генерация зон **на хосте** (без Python в контейнере).
- Работает с `docker compose up -d` сразу после копирования.
- Всё в одном каталоге.

---

## 📁 Структура проекта (скопируйте как есть)

```
bind9-dns/
├── docker-compose.yml
├── named.conf
├── zones/
│   └── db.example.local
│   └── db.10.0.2.in-addr.arpa
├── scripts/
│   └── gen_zones.py
└── run.sh
```

---

## 1. `docker-compose.yml`

```yaml
# docker-compose.yml
services:
  bind9:
    image: internetsystemsconsortium/bind9:9.18
    container_name: bind9
    restart: unless-stopped
    volumes:
      - ./named.conf:/etc/bind/named.conf:ro
      - ./zones:/etc/bind/zones:ro
    ports:
      - "53:53/tcp"
      - "53:53/udp"
    command: named -g -c /etc/bind/named.conf
```

---

## 2. `named.conf`

```conf
// named.conf
options {
    directory "/var/cache/bind";
    recursion no;
    allow-query { any; };
    listen-on { any; };
    listen-on-v6 { none; };
    dnssec-validation no;  // отключаем для простоты
};

zone "example.local" {
    type master;
    file "/etc/bind/zones/db.example.local";
};

zone "10.0.2.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.10.0.2.in-addr.arpa";
};
```

---

## 3. `scripts/gen_zones.py`

```python
#!/usr/bin/env python3
# scripts/gen_zones.py
import os
from datetime import datetime

DOMAIN = "example.local"
SERIAL = datetime.now().strftime("%Y%m%d%H")

# Прямая зона
forward = f"""$TTL 86400
@   IN  SOA ns1.{DOMAIN}. hostmaster.{DOMAIN}. (
        {SERIAL}
        3600
        1800
        1209600
        86400 )

@       IN  NS  ns1.{DOMAIN}.
ns1     IN  A   10.0.2.10
www     IN  A   10.0.2.20
mail    IN  A   10.0.2.30
"""

# PTR-зона (для сети 10.0.2.0/24)
reverse = f"""$TTL 86400
@   IN  SOA ns1.{DOMAIN}. hostmaster.{DOMAIN}. (
        {SERIAL}
        3600
        1800
        1209600
        86400 )

@   IN  NS  ns1.{DOMAIN}.
10  IN  PTR ns1.{DOMAIN}.
20  IN  PTR www.{DOMAIN}.
30  IN  PTR mail.{DOMAIN}.
"""

os.makedirs("zones", exist_ok=True)

with open("zones/db.example.local", "w") as f:
    f.write(forward.strip() + "\n")

with open("zones/db.10.0.2.in-addr.arpa", "w") as f:
    f.write(reverse.strip() + "\n")

print("✅ Зоны сгенерированы в папке zones/")
```

---

## 4. `run.sh` — скрипт запуска

```bash
#!/bin/bash
# run.sh
set -e

echo "🔄 Генерация зон..."
python3 scripts/gen_zones.py

echo "🐳 Запуск BIND9..."
docker compose down 2>/dev/null || true
docker compose up -d

echo "📋 Логи:"
docker logs bind9 --tail=20
```

Сделайте его исполняемым:

```bash
chmod +x run.sh
```

---

## 🚀 Как запустить (всё с нуля)

1. Создайте папку:
   ```bash
   mkdir bind9-dns && cd bind9-dns
   ```

2. Создайте файлы (скопируйте содержимое выше):
   ```bash
   mkdir -p scripts zones
   # ... создайте файлы через nano, vim или echo
   ```

3. Убедитесь, что у вас установлен **Python 3**:
   ```bash
   python3 --version
   ```

4. Запустите:
   ```bash
   ./run.sh
   ```

---

## 🔍 Проверка работы

### Проверка извне (на хосте):

```bash
# Прямой запрос
dig @127.0.0.1 www.example.local A +short
# Должно вернуть: 10.0.2.20

# PTR-запрос
dig @127.0.0.1 -x 10.0.2.20 +short
# Должно вернуть: www.example.local.
```

> ⚠️ Если у вас macOS или Windows — замените `127.0.0.1` на IP Docker-хоста (обычно `127.0.0.1` работает и там).

---

## 🔄 Как адаптировать под ваш домен

1. Замените `example.local` → `happylink.net.ua`
2. Замените IP-адреса:
   - `10.0.2.10` → `146.120.101.247`
   - и т.д.
3. Добавьте вторую PTR-зону в `named.conf` и `gen_zones.py`, если нужно.

Пример для двух PTR:

```python
# В gen_zones.py добавьте:
with open("zones/db.2.176.193.in-addr.arpa", "w") as f:
    f.write("""$TTL 86400
@   IN  SOA ns1.happylink.net.ua. hostmaster.happylink.net.ua. (
        2025040501
        3600
        1800
        1209600
        86400 )
@   IN  NS  ns1.happylink.net.ua.
1   IN  PTR ns1.happylink.net.ua.
""")
```

И добавьте зону в `named.conf`.

---

## 💡 Почему это работает

- Никаких `apt-get` в контейнере — только официальный образ.
- Все файлы генерируются **до запуска контейнера**.
- Конфигурация минимальна и валидна.
- Используется `dnssec-validation no` — чтобы не мешал при тестировании.


```bash
./run.sh
docker logs bind9
```
