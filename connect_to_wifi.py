import network
import time


def connect_to_internet():
    # Initialize Wi-Fi in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Connect to your Wi-Fi network
    ssid = 'Alex iPhone'
    password = 'Alex123!'

    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)

        # Wait for connection
        while not wlan.isconnected():
            time.sleep(1)

    print('Network config:', wlan.ifconfig())