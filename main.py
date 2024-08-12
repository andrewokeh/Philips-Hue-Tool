import requests
from huesdk import Hue


class Bridge:
    def __init__(self):
        bridge_info = self.get_bridge_info()
        if bridge_info:
            self.ip = bridge_info[0].get("internalipaddress")
            self.mac = bridge_info[0].get("id")
        else:
            self.ip = None
            self.mac = None

    @staticmethod
    def get_bridge_info():
        url = "https://discovery.meethue.com/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve bridge information: {e}")
            return None


def main() -> None:
    bridge = Bridge()
    if bridge.ip and bridge.mac:
        print(f"IP Address: {bridge.ip}")
        print(f"MAC Address: {bridge.mac}")
    else:
        print("No bridge information available.")


if __name__ == "__main__":
    main()
