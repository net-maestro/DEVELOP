---
# BIND9 DNS-сервер для HappyLink
#### Этот проект поднимает авторитативный DNS-сервер для домена **`happylink.net.ua`** и реверс-зон для двух подсетей /24
##### 146.120.101.0/24 193.176.2.0/24
---

```
bind9/
 ├── docker-compose.yml      # запуск контейнера BIND9
 ├── named.conf              # основной конфиг BIND9
 ├── zones/                  # DNS-зоны
 │    ├── db.happylink.com
 │    ├── db.101.120.146.in-addr.arpa
 │    ├── db.2.176.193.in-addr.arpa
 └── scripts/
      └── GEN_PTR.py         # генератор PTR-записей

```

## 🔧 Установка и запуск

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/<yourname>/happylink-dns.git
   cd happylink-dns/bind9
   ```

2. Запустить контейнер:

   ```bash
   docker-compose up -d
   ```

3. Проверить работу:

   ```bash
   dig @127.0.0.1 ns1.happylink.net.ua
   dig @127.0.0.1 -x 145.100.222.10
   ```

---

## ⚙️ Конфигурация

### Основной конфиг: `named.conf`

* Отключена рекурсия (сервер **только авторитативный**).
* Настроены три зоны:

  * `happylink.net.ua`
  * `101.120.146.in-addr.arpa`
  * `2.176.193.in-addr.arpa`

### Прямая зона: `db.happylink.com`

Содержит:

* NS-записи (`ns`, `ns1`)
* A-записи для `www`, `mail`, `api`
* MX-запись для почты

### Реверс-зоны

* `db.101.120.146.in-addr.arpa` → PTR для `ns`, `www`, `mail`
* `db.2.176.193.in-addr.arpa` → PTR для `ns1`, `api`

---

## 🔄 Автоматическая генерация PTR-зон

Для удобства есть Python-скрипт `scripts/gen_ptr.py`.

Пример генерации:

```bash
cd bind9/scripts

# Для сети 146.120.101.0/24
./gen_ptr.py 146.120.101.0 happylink.net.ua > ../zones/db.101.120.146.in-addr.arpa

# Для сети 148.100.222.0/24
./gen_ptr.py 148.100.222.0 happylink.net.ua > ../zones/db.2.176.193.in-addr.arpa
```

По умолчанию скрипт создаёт PTR-записи `hostX.happylink.com` для всех адресов от `.1` до `.254`.
Для "особых" IP (например `ns1`, `www`, `mail`, `api`) имена прописаны вручную в скрипте.

---

## 🔍 Проверка DNS

```bash
# Прямая запись
dig @127.0.0.1 www.happylink.net.ua

# PTR-запись
dig @127.0.0.1 -x 146.120.101.2
```
