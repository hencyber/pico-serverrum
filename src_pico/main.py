from wifi import connect_wifi
import time
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
import json

time.sleep(.5)

sensor = DHT11(Pin(16))
status_led = Pin(15, Pin.OUT)

MQTT_BROKER = "10.200.84.248"
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


def wait_for_wifi():
    # the radio needs time after power on, connecting again too early restarts it
    while not connect_wifi(WIFI_TRIES):
        print("Wifi did not answer, trying again")


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
