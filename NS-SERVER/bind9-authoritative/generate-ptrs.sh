#!/bin/bash
DOMAIN="happylink.net.ua"
mkdir -p zones

# Подсеть 146.120.101.0/24
cat > zones/101.120.146.in-addr.arpa.zone <<EOF
\$TTL 3600
@ IN SOA dns2.$DOMAIN. admin.$DOMAIN. (
    2025040501
    3600
    900
    604800
    3600
)
@ IN NS dns2.$DOMAIN.

EOF

for i in {1..254}; do
    # Пример: все IP ведут на generic имя (измени по желанию)
    echo "$i IN PTR ip-$i.$DOMAIN." >> zones/101.120.146.in-addr.arpa.zone
done

# Подсеть 193.176.2.0/24
cat > zones/2.176.193.in-addr.arpa.zone <<EOF
\$TTL 3600
@ IN SOA dns2.$DOMAIN. admin.$DOMAIN. (
    2025040501
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
