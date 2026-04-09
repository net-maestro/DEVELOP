import requests
import json
import time

# Конфигурация — общие параметры
API_URL = "/api/v1/component/macros/execute"
AUTH_TOKEN = ""
DEVICE_ID = 249
MACRO_ID = 26
PREVIEW = False
TSLEEP = 2
INTERFACE_NAME = "gpon_olt-1/2/8"
START_ONT_NUMBER = 24

# Данные по ONU: description, serial, up/down speed, vlan_id
# Пример: {"description":"6348","serial":"HWTC6A47BB96","up":"UP-100M","down":"DOWN-100M","vlan_id":"1116"}

ONU_DATA = [
{"description":"51004","serial":"HWTC6AB3A73F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51005","serial":"ZTEGC6A52CD7","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51010","serial":"HWTCA613E107","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51012","serial":"HWTCAF7BF3ED","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51020","serial":"ZTEGC19F0409","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51029","serial":"ZTEGC1BC1C3A","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51033","serial":"HWTC1D2B947F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51034","serial":"HWTCAFDAC23F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51035","serial":"HWTCA613DAF9","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51036","serial":"ZTEGC173BE3B","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51037","serial":"HWTCD1A35701","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51038","serial":"ZTEGC657C4B1","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51043","serial":"ZTEGC6989819","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51044","serial":"HWTC1D438DF0","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51046","serial":"ZTEGC174DFDC","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51047","serial":"ZTEGC697F2C3","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51048","serial":"HWTCA61E1091","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51054","serial":"HWTCA613DADB","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51057","serial":"HWTCAF7BF3E9","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51061","serial":"ZTEGC1AEE8EF","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51067","serial":"HWTCAF7BF3EB","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51069","serial":"ZXICC06F13AD","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51071","serial":"ZTEGC15F7350","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51073","serial":"HWTC6AB3A52F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51076","serial":"ZTEGC54234DF","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51078","serial":"HWTCD1A3565D","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51081","serial":"ZTEGC6DA6000","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51090","serial":"ZTEGC1846B07","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51093","serial":"HWTCA609D165","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51101","serial":"ZTEGC19471AF","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51102","serial":"ZTEGC690F33A","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51105","serial":"HWTCA613DAD7","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51111","serial":"ZTEGC0DD1CD3","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51118","serial":"HWTCA613DAE5","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51125","serial":"ZTEGC150E5A3","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51129","serial":"HWTC1D297B07","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51130","serial":"ZTEGC6A52629","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51131","serial":"HWTCA613E0FF","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51144","serial":"ZTEGC694DF44","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51145","serial":"ZTEGC6DC7D53","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"51147","serial":"HWTC6AB3A731","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"52008","serial":"HWTCA609D39F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"53038","serial":"ZTEGC697D0B0","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"53079","serial":"ZTEGC1B5A2FD","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"53146","serial":"HWTCAF7C4935","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"53305","serial":"ZTEGC0DD10A2","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
{"description":"53400","serial":"ZTEGC19F765F","up":"UP-100M","down":"DOWN-100M","vlan_id":"1217"},
]


HEADERS = {
    "X-Auth-Token": AUTH_TOKEN,
    "Content-Type": "application/json",
}

def register_onu(data, ont_number):
    payload = {
        "from": "device",
        "device": {"id": DEVICE_ID},
        "params": {
            "iface": INTERFACE_NAME,
            "ont_number": str(ont_number),
            "description": data["description"],
            "serial": data["serial"],
            "onu_model_gpon": "F601",
            "vlan_id": str(data["vlan_id"]),  # ← теперь из данных
            "up_speed_profile": data["up"],
            "down_speed_profile": data["down"]
        },
        "preview": PREVIEW,
        "macros": {"id": MACRO_ID}
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        status = response.status_code
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = {"raw_response": response.text}

        print(f"[{ont_number:3}] 📡 {data['description']:4} | {data['serial']:12} | VLAN {data['vlan_id']:4} → HTTP {status}")
        if status == 200:
            print(f"      ✅ Успешно")
            return True
        else:
            print(f"      ❌ Ошибка: {result}")
            return False

    except Exception as e:
        print(f"[{ont_number:3}] ❌ Ошибка запроса для {data['description']}: {e}")
        return False

def main():
    print("🚀 Начинаем регистрацию ONU (с индивидуальными VLAN)...")
    print(f"🔢 Стартовый номер ONU: {START_ONT_NUMBER}")
    print("-" * 70)
    success_count = 0

    for idx, onu in enumerate(ONU_DATA, start=1):
        ont_number = START_ONT_NUMBER + idx
        if ont_number > 128:
            print("⚠️ Достигнут лимит ONT номеров (128). Остановка.")
            break

        if register_onu(onu, ont_number):
            success_count += 1

        # Пауза — можно убрать или настроить под вашу систему
        time.sleep(TSLEEP)

    print("-" * 70)
    print(f"📈 Итого: {success_count} из {len(ONU_DATA)} зарегистрировано успешно.")

if __name__ == "__main__":
    main()

