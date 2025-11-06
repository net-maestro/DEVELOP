---

# 📦 Авторитативный DNS-сервер на BIND9 (Docker Compose)

Этот репозиторий содержит готовую конфигурацию **авторитативного DNS-сервера** на основе **ISC BIND9**, запущенного в **Docker Compose**. Сервер обслуживает:

- Прямую зону: `happylink.net.ua`
- Две обратные (PTR) зоны:
  - `146.120.101.in-addr.arpa` → для подсети `146.120.101.0/24`
  - `193.176.2.in-addr.arpa` → для подсети `193.176.2.0/24`

Рекурсия **отключена**, сервер работает **только в режиме master** для указанных зон.

---

## 📁 Структура проекта

```
bind9-authoritative/
├── README.md
├── docker-compose.yml
├── named.conf.options
├── named.conf.local
├── zones/
│   ├── happylink.net.ua.zone
│   ├── 101.120.146.in-addr.arpa.zone
│   └── 2.176.193.in-addr.arpa.zone
└── generate-ptrs.sh
```

---

## 📄 Файлы конфигурации

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  bind9:
    image: internetsystemsconsortium/bind9:9.18
    container_name: bind9
    hostname: dns2-happylink-net-ua
    ports:
      - "53:53/udp"
      - "53:53/tcp"
    volumes:
      - ./named.conf.options:/etc/bind/named.conf.options:ro
      - ./named.conf.local:/etc/bind/named.conf.local:ro
      - ./zones:/etc/bind/zones:ro
    restart: unless-stopped
```

> 🔐 Пробрасывает порт 53 (UDP/TCP) и монтирует конфигурацию в контейнер.

---

### `named.conf.options`

```conf
options {
    directory "/var/cache/bind";

    listen-on port 53 { any; };
    listen-on-v6 { none; };

    // Отключаем рекурсию — только авторитетные зоны
    recursion no;

    // Разрешаем запросы от всех (ограничьте при необходимости)
    allow-query { any; };

    // Безопасность и производительность
    auth-nxdomain yes;
    dnssec-validation no;
    version "not disclosed";
    hostname "not disclosed";
};
```

---

### `named.conf.local`

```conf
// Прямая зона
zone "happylink.net.ua" {
    type master;
    file "/etc/bind/zones/happylink.net.ua.zone";
};

// Обратные зоны (PTR)
zone "101.120.146.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/101.120.146.in-addr.arpa.zone";
};

zone "2.176.193.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/2.176.193.in-addr.arpa.zone";
};
```

---

### `zones/happylink.net.ua.zone`

```zone
$TTL 3600
@ IN SOA dns2.happylink.net.ua. admin.happylink.net.ua. (
    2025110601 ; serial — увеличивайте при каждом изменении!
    3600       ; refresh
    900        ; retry
    604800     ; expire
    3600 )     ; minimum

@       IN NS dns2.happylink.net.ua.
@       IN A  146.120.101.100   ; apex-запись (опционально)

dns2    IN A 146.120.101.252
www     IN A 146.120.101.245
mail    IN A 146.120.101.253
; Добавьте другие записи по необходимости
```

---

### `zones/101.120.146.in-addr.arpa.zone`

```zone
$TTL 3600
@ IN SOA dns2.happylink.net.ua. admin.happylink.net.ua. (
    2025110601
    3600
    900
    604800
    3600
)

@ IN NS dns2.happylink.net.ua.

245  IN PTR www.happylink.net.ua.
252  IN PTR dns2.happylink.net.ua.
253  IN PTR mail.happylink.net.ua.
; Добавляйте по мере необходимости
```

---

### `zones/2.176.193.in-addr.arpa.zone`

```zone
$TTL 3600
@ IN SOA dns2.happylink.net.ua. admin.happylink.net.ua. (
    2025110601
    3600
    900
    604800
    3600
)

@ IN NS dns2.happylink.net.ua.

1   IN PTR server1.happylink.net.ua.
2   IN PTR server2.happylink.net.ua.
; Добавляйте нужные PTR-записи
```

> ⚠️ **Важно**: имена в PTR **должны заканчиваться точкой** (`.`), иначе будут интерпретироваться как относительные.

---

### `generate-ptrs.sh` — генератор PTR-записей (опционально)

> ⚠️ Этот скрипт **перезаписывает** файлы зон! Используйте с осторожностью.

```bash
#!/bin/bash
DOMAIN="happylink.net.ua"
mkdir -p zones

# Подсеть 146.120.101.0/24
cat > zones/101.120.146.in-addr.arpa.zone <<EOF
\$TTL 3600
@ IN SOA dns2.$DOMAIN. admin.$DOMAIN. (
    2025110601
    3600
    900
    604800
    3600
)
@ IN NS dns2.$DOMAIN.

EOF

for i in {1..254}; do
    echo "$i IN PTR ip-$i.$DOMAIN." >> zones/101.120.146.in-addr.arpa.zone
done

# Подсеть 193.176.2.0/24
cat > zones/2.176.193.in-addr.arpa.zone <<EOF
\$TTL 3600
@ IN SOA dns2.$DOMAIN. admin.$DOMAIN. (
    2025110601
    3600
    900
    604800
    3600
)
@ IN NS dns2.$DOMAIN.

EOF

for i in {1..254}; do
    echo "$i IN PTR ip2-$i.$DOMAIN." >> zones/2.176.193.in-addr.arpa.zone
done

echo "PTR-зоны сгенерированы в ./zones/"
```

Сделайте исполняемым:
```bash
chmod +x generate-ptrs.sh
```

---

## ▶️ Запуск

1. **Клонируйте или создайте репозиторий**:
   ```bash
   git clone https://github.com/ваш-логин/bind9-authoritative.git
   cd bind9-authoritative
   ```

2. **Проверьте и при необходимости отредактируйте** зоны (`zones/*.zone`).

3. **Запустите контейнер**:
   ```bash
   docker compose up -d
   ```

4. **Проверьте логи**:
   ```bash
   docker logs bind9
   ```
   Успешная загрузка зон выглядит так:
   ```
   zone happylink.net.ua/IN: loaded serial 2025110601
   ```

5. **Проверьте синтаксис (опционально)**:
   ```bash
   docker exec bind9 named-checkconf
   docker exec bind9 named-checkzone happylink.net.ua /etc/bind/zones/happylink.net.ua.zone
   ```

---

## 🔍 Тестирование

```bash
# Прямой запрос
dig @127.0.0.1 www.happylink.net.ua A +short

# Обратный запрос (PTR)
dig @127.0.0.1 -x 146.120.101.252 +short

# Проверка NS
dig @127.0.0.1 happylink.net.ua NS +short
```

> Если вы тестируете **удалённо**, замените `127.0.0.1` на IP хоста с запущенным сервером.

---

## ⚠️ Важные замечания

- **Serial в SOA должен увеличиваться** при каждом изменении зоны, иначе вторичные сервера не подтянут обновления.
- Убедитесь, что **порт 53 свободен** на хосте (`sudo ss -tulnp | grep :53`).
- Для публичного использования: настройте делегирование NS-записей у регистратора домена.
- В продакшене: ограничьте `allow-query { trusted-nets; };` вместо `{ any; }`.

---

## 📜 Лицензия

MIT License — свободно используйте, изменяйте и распространяйте.

---

## 🤝 Поддержка

Если что-то не работает:
1. Проверьте логи (`docker logs bind9`)
2. Убедитесь, что все имена в зонах заканчиваются точкой
3. Увеличьте serial при изменении зоны
4. Убедитесь, что файлы зон **читаемы** (права 644)

---

Готово! Теперь вы можете:
```bash
git init
git add .
git commit -m "Initial commit: authoritative BIND9 DNS server"
git remote add origin https://github.com/ваш-логин/bind9-authoritative.git
git push -u origin main
```

Если нужно — могу сгенерировать `.gitignore`, `LICENSE` или автоматизировать деплой.
