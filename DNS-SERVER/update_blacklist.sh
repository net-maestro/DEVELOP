#!/bin/bash

# Путь к конфигурационному файлу blacklist.conf
BLACKLIST_FILE="./unbound/blacklist.conf"

# URL для загрузки списка доменов
URL="https://uablacklist.net/domains.txt"

# Домен, на который будет происходить редирект
REDIRECT_DOMAIN="block.happylink.net.ua"

# Загрузка списка доменов
echo "Загрузка списка доменов..."
curl -s $URL -o domains.txt

# Проверка успешности загрузки
if [ $? -ne 0 ]; then
    echo "Ошибка при загрузке списка доменов. Проверьте URL."
    exit 1
fi

# Генерация конфигурации для Unbound
echo "Создание нового blacklist.conf..."
echo "# Generated on $(date)" > $BLACKLIST_FILE
while read -r DOMAIN; do
    if [[ ! -z "$DOMAIN" && ! "$DOMAIN" =~ ^# ]]; then
        echo "local-zone: \"$DOMAIN\" redirect" >> $BLACKLIST_FILE
        echo "local-data: \"$DOMAIN CNAME $REDIRECT_DOMAIN.\"" >> $BLACKLIST_FILE
    fi
done < domains.txt

# Удаление временного файла
rm -f domains.txt

echo "Обновление завершено. Перезапуск контейнера Unbound..."
#docker-compose restart unbound

#Обновление корневых доменов 
curl -o ./unbound/root.hints https://www.internic.net/domain/named.root
echo "Обновление корневых доменов."

echo "Blacklist успешно обновлен и применен."
