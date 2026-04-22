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


def normalize_port(port: str) -> str:
    """
    Приводит:
    vport-1/1/4.8:1 → gpon-onu_1/1/4:8
    """

    if port.startswith("gpon-onu_"):
        return port

    if port.startswith("vport-"):
        # вытаскиваем часть после vport-
        raw = port.replace("vport-", "")

        # 1/1/4.8:1
        match = re.match(r'(\d+/\d+/\d+)\.(\d+):\d+', raw)
        if match:
            pon = match.group(1)   # 1/1/4
            onu = match.group(2)   # 8

            return f"gpon-onu_{pon}:{onu}"

    return port  # fallback



def parse_zxan_mac(output: str):
    """
    Универсальный парсер под разные форматы ZTE
    """

    for line in output.splitlines():
        line = line.strip()

        # ищем строку с MAC
        if re.search(r'[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}', line, re.I):
            parts = line.split()

            if len(parts) >= 4:
                mac = parts[0].lower()
                raw_port = parts[3]

                port = normalize_port(raw_port)

                return {
                    'mac_usr': mac,
                    'pon_port': port
                }

    return None


def get_free_ip():
    """Получает свободный IP из API"""
    try:
        response = requests.get(FREE_IP, timeout=5)
        response.raise_for_status()
        data = response.json()

        free_ip_list = data.get('free_ip', [])
        if isinstance(free_ip_list, list) and len(free_ip_list) > 0:
            return free_ip_list[0].get('free_ip')

        return None

    except Exception as e:
        print(f"Ошибка получения IP: {e}")
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
WHERE b.switch=420 AND cl.agreement IN ( 
   51004
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

    mac_db = row['mac']
    mac_zxan = mac_to_zxan(mac_db)

    print(f"\n=== Обработка MAC {mac_db} ===")

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
        print(f"Найдено на OLT: {parsed}")

        free_ip = get_free_ip()
        if not free_ip:
            print("⚠️ Не удалось получить IP, пропускаем")
            continue

        print(f"✓ Новый IP: {free_ip}")

        update_sql = """
            UPDATE eq_bindings
            SET switch = %s, port = %s, ip = %s
            WHERE switch = %s AND mac = %s
        """

        cursor.execute(
            update_sql,
            ("430", parsed['pon_port'], free_ip, "420", mac_db)
        )
        conn.commit()

        print(f"✓ Обновлено → port={parsed['pon_port']}")

    else:
        print(f"✗ MAC не найден на OLT")

# ================== CLEANUP ==================

cursor.close()
conn.close()

print("\n=== Готово! ===")
