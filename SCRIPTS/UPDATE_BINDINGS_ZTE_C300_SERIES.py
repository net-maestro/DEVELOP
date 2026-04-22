import os
import re
import requests
from TELNET2 import Sw_telnet as SW
from DB import db as db_connect
from dotenv import load_dotenv

# ================== ENV ==================
load_dotenv()

SW_LOGIN = os.getenv('SW_LOGIN')
SW_PASSWD = os.getenv('SW_PASSWD')

OLT_IP = '172.16.1.200'

FREE_IP = 'https://provider.net.ua/netcontrol/api/get-free-ip?vlan_name=1217'

# ================== HELPERS ==================
def mac_to_zxan(mac: str) -> str:
    """
    04:D9:F5:18:8F:30 -> 04D9.F518.8F30
    """
    mac = mac.replace(':', '').upper()
    return f"{mac[0:4]}.{mac[4:8]}.{mac[8:12]}"


def parse_zxan_mac(output: str):
    pattern = re.compile(
    r'(?P<mac>[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+'
    r'\d+\s+\w+\s+'
    r'(?P<port>g?pon-onu_\d+/\d+/\d+:\d+)',
    re.IGNORECASE
    )

    match = pattern.search(output)
    if not match:
        return None

    return {
        'mac_usr': match.group('mac').lower(),
        'pon_port': match.group('port')
    }


def get_free_ip():
    """Получает свободный IP из API"""
    try:
        response = requests.get(FREE_IP)
        response.raise_for_status()
        data = response.json()

        # Структура: {"free_ip": [{"free_ip": "172.16.217.61"}], "status": "success"}
        free_ip_list = data.get('free_ip', [])
        if isinstance(free_ip_list, list) and len(free_ip_list) > 0:
            ip = free_ip_list[0].get('free_ip')
            return ip

        return None
    except Exception as e:
        print(f"Ошибка получения IP: {e}")
        import traceback
        traceback.print_exc()
        return None

# ================== DB ==================


sql = """
SELECT
    b.switch,
    b.mac,
    b.port,
    b.ip
FROM eq_bindings b
JOIN client_prices act ON act.id = b.activation
JOIN clients cl ON cl.id = act.agreement
WHERE b.switch=265 AND cl.agreement IN (
   51004, 51005, 51010, 51020, 51029, 51034, 51035, 51036,
    51037, 51038, 51043, 51044, 51046, 51047, 51048, 51054, 51057, 51061,
    51067, 51069, 51071, 51073, 51076, 51078, 51081, 51090, 51093, 51101,
    51102, 51105, 51111, 51118, 51125, 51129, 51130, 51131, 51144, 51145,
    51147, 52008, 53038, 53079, 53146, 53305, 53400
);
"""

conn = db_connect()
cursor = conn.cursor()
cursor.execute(sql)

rows = cursor.fetchall()
if not rows:
    raise Exception('Записи в eq_bindings не найдены')

columns = [col[0] for col in cursor.description]

print(f"Найдено записей для обработки: {len(rows)}")


# ================== MAIN ==================
for row_raw in rows:
    row = dict(zip(columns, row_raw))

    mac_db = row['mac']                     # 04:D9:F5:18:8F:30
    mac_zxan = mac_to_zxan(mac_db)          # 04D9.F518.8F30

    sw = SW(
        OLT_IP,
        2,
        SW_LOGIN,
        SW_PASSWD,
        [
            'terminal length 0',
            f'show mac {mac_zxan}'
        ]
    )

    output = sw.get_output()
    parsed = parse_zxan_mac(output)

    if parsed:
        print(f"Найдена запись на OLT: {parsed}")

        # ================== ПОЛУЧАЕМ НОВЫЙ IP ПЕРЕД КАЖДЫМ UPDATE ==================
        free_ip = get_free_ip()
        if not free_ip:
            print(f"⚠️  Не удалось получить свободный IP для MAC {mac_db}, пропускаем...")
            continue

        print(f"✓ Получен новый IP: {free_ip}")

        # ================== UPDATE ==================
        update_sql = """
            UPDATE eq_bindings
            SET switch = %s, port = %s, ip = %s
            WHERE switch = %s AND mac = %s
        """
        cursor.execute(update_sql, ("265", parsed['pon_port'], free_ip, "265", mac_db))
        conn.commit()
        print(f"✓ Обновлено: switch=265, port={parsed['pon_port']}, ip={free_ip}")
    else:
        print(f"✗ MAC {mac_db} не найден на OLT.")

# ================== CLEANUP ==================
cursor.close()
conn.close()

print("\n=== Готово! ===")


