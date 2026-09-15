from wifi import connect_wifi
import time
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
import json

time.sleep(.5)

# hardware
sensor = DHT11(Pin(16))
green_led = Pin(15, Pin.OUT)
red_led = Pin(14, Pin.OUT)

# our mosquitto broker runs in docker on Henriks laptop
MQTT_BROKER = "192.168.1.141"
TOPIC = b"pico/serverroom/dht11"
DEVICE_ID = "pico-serverroom-01"

# thresholds for the server room
TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60
SLEEP_TIME = 3


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def show_status(status):
    # green led when everything is fine, red led when it is not
    green_led.value(1 if status == "OK" else 0)
    red_led.value(1 if status == "ALARM" else 0)


def connect_mqtt():
    client = MQTTClient(client_id=DEVICE_ID, server=MQTT_BROKER, port=1883)
    client.connect()
    print("Connected to MQTT")
    return client


green_led.value(0)
red_led.value(0)

if not connect_wifi():
    # blink red led so we see that something is wrong before we give up
    for _ in range(5):
        red_led.toggle()
        time.sleep(.5)
    raise Exception("Could not connect to wifi")

client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
    except OSError:
        # the dht11 sometimes fails to answer, then we just try again
        print("Could not read the sensor, trying again")
        time.sleep(SLEEP_TIME)
        continue

    status = get_status(temperature, humidity)
    show_status(status)

    data = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
        "status": status,
    }
    payload = json.dumps(data)
    client.publish(TOPIC, payload)

    print(f"sent: {payload} to mosquitto")
    time.sleep(SLEEP_TIME)
