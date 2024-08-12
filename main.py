import requests
import os
from huesdk import Hue
import time
from random import randint


class Bridge:
    def __init__(self):
        # bridge_info = self.get_bridge_info() # Only make one request every 15 minutes!
        bridge_info = [{"id": os.getenv("BRIDGEMAC"), "internalipaddress": os.getenv("BRIDGEIP"), "port": "443"}]
        if bridge_info:
            self.ip = bridge_info[0].get("internalipaddress")
            self.mac = bridge_info[0].get("id")
            # self.username = Hue.connect(bridge_ip=self.ip) # Must press link button on bridge to generate username
            self.username = os.getenv("BRIDGEUSERNAME")
        else:
            self.ip = None
            self.mac = None
            self.username = None

    @staticmethod
    def get_bridge_info():
        """
        Get Philips Hue Bridge info. Rate limited to one request every 15 minutes.
        :rtype: JSON data with MAC, IP, port
        """
        # Might eventually use ARP to find device using OUI on local network instead, to avoid rate limiting
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
        print(f"Bridge IP Address: {bridge.ip}")
        print(f"Bridge MAC Address: {bridge.mac}")
    else:
        print("No bridge information available.")

    hue = Hue(bridge_ip=bridge.ip, username=bridge.username)

    lights = hue.get_lights()
    for _ in range(100):  # Randomly change hue of all lights every second
        print(_)
        for light in lights:
            light.set_color(hue=randint(0, 65535))
        time.sleep(1)


if __name__ == "__main__":
    main()
