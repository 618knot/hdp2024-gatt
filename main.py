import dbus
import logging
from bluezero import peripheral
from bluezero import adapter
import subprocess
import json
from joystick import Joystick

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)

DEVICE_NAME = "namekawa"

# UUIDの定義
SERVICE_UUID = '96a3093b-708c-4abd-97d2-9d8b10c122ec'
CHAR_UUID = '206ff6bf-5f3e-4c9e-902f-b7762595ddd8'

joystick = Joystick()

# コールバック関数
def char_read(value):
    logging.debug('Characteristic read: {}'.format(value))
    global rotation_json
    rotation_json = json_str(joystick.get_values())
    return rotation_json

def json_str(dict_val: dict):
    return bytearray(json.dumps(dict_val), "utf-8")

# 特性の初期値
rotation_json = json_str(joystick.get_values())

def char_write(value):
    global rotation_json
    logging.debug('Characteristic write: {}'.format(value))
    rotation_json = value

# システム情報を取得
def get_system_info():
    info = {}
    info['bluetooth_status'] = subprocess.getoutput('systemctl is-active bluetooth')
    info['dbus_status'] = subprocess.getoutput('systemctl is-active dbus')
    info['bluez_version'] = subprocess.getoutput('bluetoothctl --version')
    return info

# 利用可能なBluetoothアダプタを取得
def get_bluetooth_adapter():
    try:
        adapters = adapter.list_adapters()
        if adapters:
            return adapters[0]
        else:
            logging.error("No Bluetooth adapters found.")
            return None
    except Exception as e:
        logging.error(f"Error getting Bluetooth adapter: {e}")
        return None

# メイン処理
def main():
    # システム情報を表示
    system_info = get_system_info()
    logging.info(f"System info: {system_info}")

    # Bluetoothアダプタの取得
    adapter_address = get_bluetooth_adapter()
    if adapter_address is None:
        raise Exception("No Bluetooth adapter found")

    logging.info(f"Using Bluetooth adapter: {adapter_address}")

    try:
        # Peripheral の設定
        my_peripheral = peripheral.Peripheral(adapter_address, local_name=f'hdp2024-{DEVICE_NAME}')

        # サービスの追加
        my_peripheral.add_service(1, SERVICE_UUID, True)

        # 特性の追加
        my_peripheral.add_characteristic( 
            srv_id=1,
            chr_id=1,
            uuid=CHAR_UUID,
            value=rotation_json,
            notifying=False,
            flags=['read', 'write'],
            read_callback=char_read,
            write_callback=char_write)

        # アドバタイジングの開始
        my_peripheral.publish()

    except dbus.exceptions.DBusException as e:
        logging.error(f"DBus error: {e}")
        logging.info("Please check if bluetoothd is running and you have the necessary permissions.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        joystick.close()
        print("stop")

if __name__ == "__main__":
    main()