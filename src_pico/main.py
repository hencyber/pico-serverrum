from wifi import connect_wifi
import time
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
import json

time.sleep(.5)

with open("wifi_credentials.json") as file:
    config = json.load(file)

sensor = DHT11(Pin(16))
status_led = Pin(15, Pin.OUT)

# the broker address changes every time we switch network, so we keep it in
# wifi_credentials.json instead of here. that file is not in git
MQTT_BROKER = config["MQTT_BROKER"]
TOPIC = b"pico/serverroom/dht11"
DEVICE_ID = "pico-serverroom-01"

TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60
SLEEP_TIME = 3
# connect_wifi waits two seconds per try, so this is 90 seconds
WIFI_TRIES = 45


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def show_status(status, seconds):
    # the led shines when everything is ok and blinks when there is an alarm
    if status == "OK":
        status_led.value(1)
        time.sleep(seconds)
    else:
        for _ in range(int(seconds * 4)):
            status_led.toggle()
            time.sleep(.25)
        status_led.value(0)


def show_networks():
    # the pico radio only uses channel 1 to 11. if the network sits on 12 or 13
    # it is invisible here no matter how strong the signal is, so we print what
    # we can actually see to make that obvious
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Networks the pico can see:")
    found = False
    for ssid, bssid, channel, rssi, auth, hidden in wlan.scan():
        name = ssid.decode("utf-8", "replace")
        if name:
            print(f"   {name}  channel {channel}  {rssi} dBm")
        if name == config["WIFI_SSID"]:
            found = True

    if not found:
        print("The network in wifi_credentials.json is NOT in the list.")
        print("Either the name is wrong or the network is on channel 12 or 13.")
        print("Turn the hotspot off and on so it picks another channel.")


def wait_for_wifi():
    # the radio needs time after power on, connecting again too early restarts it
    while not connect_wifi(WIFI_TRIES):
        print("Wifi did not answer, trying again")
        show_networks()


def connect_mqtt():
    while True:
        try:
            client = MQTTClient(client_id=DEVICE_ID, server=MQTT_BROKER, port=1883)
            client.connect()
            print("Connected to MQTT")
            return client
        except OSError:
            print("Could not reach the broker, trying again")
            time.sleep(5)


status_led.value(0)
wait_for_wifi()
client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
    except OSError:
        # the dht11 does not answer every time
        print("Could not read the sensor, trying again")
        time.sleep(SLEEP_TIME)
        continue

    status = get_status(temperature, humidity)

    data = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "status": status,
    }
    payload = json.dumps(data)

    try:
        client.publish(TOPIC, payload)
        print(f"sent: {payload} to mosquitto")
    except OSError:
        print("Could not send, connecting again")
        wait_for_wifi()
        client = connect_mqtt()
        continue

    show_status(status, SLEEP_TIME)
