import os
import json
import time
import requests

# Конфигурация — общие параметры
API_URL = "https://sw2.golden.net.ua/api/v1/component/macros/execute"
AUTH_TOKEN = "9fae3314-a913-4db1-9013-5ec3da3a1321"  # ⚠️ обязательно замените!
DEVICE_ID = 249
MACRO_ID = 26
PREVIEW = False
TSLEEP = 2
INTERFACE_NAME = "gpon_olt-1/2/3"
ONU_FILE = "onu_files/gpon_olt-1_2_3.json"
START_ONT_NUMBER = 0

# Данные по ONU: description, serial, up/down speed, vlan_id
# Пример: {"description":"6348","serial":"HWTC6A47BB96","up":"UP-100M","down":"DOWN-100M","vlan_id":"1116"}

# ---------- Загрузка данных ----------
def load_onu_data():
    if not os.path.exists(ONU_FILE):
        raise FileNotFoundError(f"Файл {ONU_FILE} не найден")

    try:
        with open(ONU_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise Exception(f"Ошибка чтения JSON: {e}")

    # базовая валидация
    for i, onu in enumerate(data, 1):
        for key in ["description", "serial", "sp", "vlan_id"]:
            if key not in onu:
                raise ValueError(f"Ошибка в записи #{i}: нет поля '{key}'")

    return data

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
    print("🚀 Загрузка ONU из JSON...")
    ONU_DATA = load_onu_data()

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






