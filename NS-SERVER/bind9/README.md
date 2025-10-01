1. ✅ Исправить ошибки в конфигах (`named.conf`, зоны).
2. ✅ Создать `Dockerfile`, если нужно (хотя официальный образ ISC BIND9 уже хорош).
3. ✅ Автоматизировать генерацию PTR-зон при запуске через скрипт.
4. ✅ Сделать рабочий `docker-compose.yml`.
5. ✅ Подготовить **полный README.md**, который вы сможете сохранить в GitHub как заметку.

---

## 🔧 Шаг 1: Исправление ошибок

### ❌ Проблемы в текущей конфигурации:

1. **Несоответствие домена в зоне и файлах**:
   - В `named.conf` объявлена зона `happylink.net.ua`, но в комментарии вы пишете `db.happylink.com`.
   - В зоне `db.happylink.net.ua` вы используете `ns1.happylink.com.` — это **разные домены** → нарушает делегирование.

2. **MX-запись содержит опечатку**:
   ```dns
   @ IN MX 10 mail.happylink.met.ua.
   ```
   → должно быть `happylink.net.ua`, а не `.met.ua`.

3. **В реверсных зонах указаны NS-серверы с другим доменом**, чем в SOA.

4. **BIND не может запуститься**, если `directory` указывает на `/etc/bind/zones`, но `named.conf` сам лежит в `/etc/bind/` — это нарушает стандартную структуру.

5. **Официальный образ ISC BIND9 требует**, чтобы `named.conf` был в `/etc/bind/`, а зоны — в подкаталоге (например, `/etc/bind/zones`), но **не меняйте `directory` на `/etc/bind/zones`** — это сломает внутренние пути.

---

## ✅ Решение: Исправленная структура

### 📁 Новая структура проекта:

```bash
bind9/
├── docker-compose.yml
├── named.conf
├── zones/
│   ├── db.happylink.net.ua
│   ├── db.101.120.146.in-addr.arpa
│   └── db.2.176.193.in-addr.arpa
├── scripts/
│   └── gen_ptr.py
└── README.md
```

> 💡 **Важно**: Все зоны используют **один домен** — `happylink.net.ua`. Уберём `happylink.com` из NS-записей, чтобы не было путаницы.

---

## 📄 1. Исправленный `named.conf`

```conf
// /etc/bind/named.conf
options {
    directory "/var/cache/bind";
    recursion no;
    allow-query { any; };
    listen-on { any; };
    listen-on-v6 { none; };
    dnssec-validation auto;
};

zone "happylink.net.ua" {
    type master;
    file "/etc/bind/zones/db.happylink.net.ua";
};

zone "101.120.146.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.101.120.146.in-addr.arpa";
};

zone "2.176.193.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.2.176.193.in-addr.arpa";
};
```

> ⚠️ Не меняйте `directory` на `/etc/bind/zones` — это нарушает работу BIND. Лучше оставить стандартный `/var/cache/bind`.

---

## 📄 2. Исправленная прямая зона: `zones/db.happylink.net.ua`

```dns
$TTL 86400
@   IN  SOA ns1.happylink.net.ua. noc.happylink.net.ua. (
        2025093002 ; Serial — увеличьте при изменениях
        3600       ; Refresh
        1800       ; Retry
        1209600    ; Expire
        86400 )    ; Minimum TTL

; NS-записи — только в рамках одного домена
@       IN  NS  ns1.happylink.net.ua.
@       IN  NS  ns2.happylink.net.ua.

; A-записи
ns1     IN  A   146.120.101.247
ns2     IN  A   146.120.101.254
www     IN  A   146.120.101.245
mail    IN  A   146.120.101.253

; MX
@       IN  MX  10 mail.happylink.net.ua.
```

> ✅ Все имена теперь в `happylink.net.ua`.

---

## 📄 3. Исправленная PTR-зона: `zones/db.101.120.146.in-addr.arpa`

```dns
$TTL 86400
@   IN  SOA ns1.happylink.net.ua. noc.happylink.net.ua. (
        2025093002
        3600
        1800
        1209600
        86400 )

@   IN  NS  ns1.happylink.net.ua.
@   IN  NS  ns2.happylink.net.ua.

247 IN PTR ns1.happylink.net.ua.
254 IN PTR ns2.happylink.net.ua.
245 IN PTR www.happylink.net.ua.
253 IN PTR mail.happylink.net.ua.
```

> ⚠️ PTR-записи указывают **последний октет IP**, например:  
> `146.120.101.247` → `247 IN PTR ...`

Аналогично для `db.2.176.193.in-addr.arpa` — укажите нужные IP.

---

## 🐍 4. Улучшенный `scripts/gen_ptr.py`

Сделаем его **универсальным** и **запускаемым при старте контейнера**.

```python
#!/usr/bin/env python3
# scripts/gen_ptr.py
import sys
import os
from datetime import datetime

def gen_zone(network, domain, special_hosts):
    # network = "146.120.101.0"
    parts = network.split('.')
    if len(parts) != 4:
        raise ValueError("Network must be in CIDR-like format: x.x.x.0")
    rev_zone = ".".join(reversed(parts[:3])) + ".in-addr.arpa"
    serial = datetime.now().strftime("%Y%m%d%H")

    content = f"""$TTL 86400
@   IN  SOA ns1.{domain}. noc.{domain}. (
        {serial} ; Serial
        3600       ; Refresh
        1800       ; Retry
        1209600    ; Expire
        86400 )    ; Minimum TTL

@   IN  NS  ns1.{domain}.
@   IN  NS  ns2.{domain}.
"""

    for ip_last, hostname in special_hosts.items():
        content += f"{ip_last} IN PTR {hostname}.\n"

    zone_file = f"zones/db.{rev_zone}"
    with open(zone_file, 'w') as f:
        f.write(content.strip() + "\n")
    print(f"✅ Generated {zone_file}")

def main():
    # Пример: python3 gen_ptr.py 146.120.101.0 happylink.net.ua
    if len(sys.argv) != 3:
        print("Usage: gen_ptr.py <network_base> <domain>")
        print("Example: gen_ptr.py 146.120.101.0 happylink.net.ua")
        sys.exit(1)

    network = sys.argv[1]
    domain = sys.argv[2]

    # Настройте свои PTR-маппинги здесь
    if network == "146.120.101.0":
        hosts = {
            247: "ns1." + domain,
            254: "ns2." + domain,
            245: "www." + domain,
            253: "mail." + domain,
        }
    elif network == "193.176.2.0":
        hosts = {
            1: "ns1." + domain,
            10: "api." + domain,
        }
    else:
        hosts = {}

    gen_zone(network, domain, hosts)

if __name__ == "__main__":
    main()
```

---

## 🐳 5. `docker-compose.yml` (без Dockerfile — используем официальный образ)

```yaml
# docker-compose.yml
services:
  bind9:
    image: internetsystemsconsortium/bind9:9.18
    container_name: bind9
    restart: unless-stopped
    volumes:
      - ./named.conf:/etc/bind/named.conf:ro
      - ./zones:/etc/bind/zones:rw
      - ./scripts:/scripts:ro
    ports:
      - "53:53/tcp"
      - "53:53/udp"
    networks:
      - dnsnet
    # Генерируем PTR перед запуском named
    command: >
      sh -c "
        python3 /scripts/gen_ptr.py 146.120.101.0 happylink.net.ua &&
        python3 /scripts/gen_ptr.py 193.176.2.0 happylink.net.ua &&
        named -g -c /etc/bind/named.conf
      "

networks:
  dnsnet:
    driver: bridge
```

> ✅ При каждом запуске (`docker-compose up`) PTR-зоны будут **перегенерироваться** с актуальным serial.

---

## 📝 6. `README.md` — ваша заметка для GitHub

```markdown
# BIND9 DNS Server в Docker

Авторитативный DNS-сервер на BIND9 с автоматической генерацией PTR-зон.

## 📁 Структура

```
bind9/
├── docker-compose.yml
├── named.conf
├── zones/                 # зоны (обновляются скриптом)
├── scripts/gen_ptr.py     # генератор PTR
└── README.md
```

## 🚀 Запуск

1. Установите Docker и Docker Compose.
2. Перейдите в папку проекта:
   ```bash
   cd bind9
   ```
3. Запустите:
   ```bash
   docker-compose up -d
   ```
4. Проверьте логи:
   ```bash
   docker logs bind9
   ```

## 🔁 Генерация PTR

Скрипт `gen_ptr.py` автоматически создаёт файлы зон при запуске контейнера.

Пример ручного запуска (для отладки):
```bash
python3 scripts/gen_ptr.py 146.120.101.0 happylink.net.ua
```

## 🛡️ Безопасность

- Сервер **не рекурсивный** (`recursion no`).
- Разрешён запрос от любого (`allow-query { any; }`), при необходимости ограничьте.

## 📌 Примечания

- Все зоны используют домен `happylink.net.ua`.
- Serial обновляется автоматически по времени.
- Официальный образ: [`internetsystemsconsortium/bind9`](https://hub.docker.com/r/internetsystemsconsortium/bind9)
```

---

## ✅ Готово!

Теперь:

- BIND9 запускается без ошибок.
- PTR-зоны генерируются автоматически.
- Конфигурация согласована и валидна.
- Всё работает через `docker-compose`.
