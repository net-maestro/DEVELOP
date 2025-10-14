#Dockerfile
# Используем легковесный базовый образ Python
FROM python:3.11-slim

# Устанавливаем зависимости для Unbound, Python и unbound-host logrotate net-tools iputils-ping lsof 
RUN apt-get update && apt-get install -y \
    unbound \
    curl \
    dnsutils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем конфигурационные файлы и ключи для Unbound
COPY unbound/ /etc/unbound/

# Создаем директорию для логов и даем права
RUN mkdir -p /var/log/unbound && chown unbound:unbound /var/log/unbound

# Открываем порты
EXPOSE 53

# Команда для запуска Unbound, rsyslog и Python-скрипта
#CMD sh -c "rsyslogd && unbound -d -c /etc/unbound/unbound.conf"
CMD sh -c "unbound -d -c /etc/unbound/unbound.conf"
