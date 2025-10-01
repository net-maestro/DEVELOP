# db.happylink.net.ua
$TTL 86400
@   IN  SOA ns.happylink.net.ua. noc.happylink.net.ua. (
        2025093001 ; Serial
        3600       ; Refresh
        1800       ; Retry
        1209600    ; Expire
        86400 )    ; Minimum TTL

; NS-записи
@       IN  NS  ns1.happylink.com.
@       IN  NS  ns2.happylink.com.

; Серверы DNS
ns     IN  A   146.120.101.254
ns1     IN  A   146.120.101.247

; Сервисы
www     IN  A   146.120.101.245
mail    IN  A   146.120.101.253

; MX-запись
@       IN  MX  10 mail.happylink.met.ua.
