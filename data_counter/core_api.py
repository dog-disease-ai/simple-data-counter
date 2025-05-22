import configparser
import requests
from dataclasses import dataclass


@dataclass
class DeviceUser:
    id: str


def get_core_api_token(config_path="core_api_config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)
    url = config["core-api"]["url"].rstrip("/")
    client_id = config["core-api"]["client_id"]
    client_secret = config["core-api"]["client_secret"]
    resp = requests.post(
        f"{url}/api/v1/auth/issue",
        json={"client_id": client_id, "client_secret": client_secret},
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["data"]["access_token"]


def get_device_user(
    device_type, device_id, config_path="core_api_config.ini"
) -> DeviceUser:
    config = configparser.ConfigParser()
    config.read(config_path)
    url = config["core-api"]["url"].rstrip("/")
    token = get_core_api_token(config_path)
    api_url = f"{url}/api/v1/devices/types/{device_type}/id/{device_id}/device-user"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    resp = requests.get(api_url, headers=headers, timeout=10)
    resp.raise_for_status()
    id = resp.json()["data"]["device_user_id"]
    if id is None:
        raise ValueError("Device user ID not found in the response.")
    return DeviceUser(id=id)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python core-api.py <device_type> <device_id>")
        sys.exit(1)
    device_type, device_id = sys.argv[1], sys.argv[2]
    user_info = get_device_user(device_type, device_id)
    print(user_info)
