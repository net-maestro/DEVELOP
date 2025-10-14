#!/bin/bash

# Подсети
SUBNETS=("146.120.101" "193.176.2")
DOMAIN="happylink.net.ua"

# Папка для конфигурационных файлов
OUTPUT_DIR="./unbound"

# Создаем папку, если её нет
mkdir -p $OUTPUT_DIR

# Генерация PTR-записей
for SUBNET in "${SUBNETS[@]}"; do
    # Извлекаем первые три октета подсети в обратном порядке
    REVERSE_SUBNET=$(echo "$SUBNET" | awk -F. '{print $3"."$2"."$1}')
    OUTPUT_FILE="${OUTPUT_DIR}/${SUBNET//./-}.conf"
    > $OUTPUT_FILE

    for i in {1..254}; do
        IP="${SUBNET}.${i}"
        PTR_NAME="${IP}.${DOMAIN}."
        REVERSE_PTR="${i}.${REVERSE_SUBNET}.in-addr.arpa."
        echo "local-data: \"${REVERSE_PTR} IN PTR ${PTR_NAME}\"" >> $OUTPUT_FILE
    done
    echo "Сгенерирован файл: $OUTPUT_FILE"
done
