import os
from TELNET2 import Sw_telnet as SW
from dotenv import load_dotenv

# ================== ENV ==================
load_dotenv()

SW_LOGIN = os.getenv('SW_LOGIN')
SW_PASSWD = os.getenv('SW_PASSWD')

OLT_IP = '172.16.1.200'

# ================== НАСТРОЙКИ ==================

PON_PORT = "gpon-onu_1/2/1"   # ← меняешь тут
ONU_RANGE = range(1, 129)     # 1–128

# ================== MAIN ==================

for onu_id in ONU_RANGE:
    full_onu = f"{PON_PORT}:{onu_id}"

    print(f"\n=== Ребут ONU {full_onu} ===")

    try:
        sw = SW(
            OLT_IP,
            2,
            SW_LOGIN,
            SW_PASSWD,
            [
                'configure terminal',
                f'pon-onu-mng {full_onu}',
                'reboot',
                'y',
                'exit',
                'exit'
            ]
        )

        output = sw.get_output()

        print(f"✓ Отправлен reboot для {full_onu}")

    except Exception as e:
        print(f"✗ Ошибка на {full_onu}: {e}")

print("\n=== Готово ===")
