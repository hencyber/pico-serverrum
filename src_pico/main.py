from wifi import connect_wifi
import time
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
import json

time.sleep(.5)

# hardware
sensor = DHT11(Pin(16))
status_led = Pin(15, Pin.OUT)

# our mosquitto broker runs in docker on Henriks laptop
MQTT_BROKER = "192.168.68.56"
TOPIC = b"pico/serverroom/dht11"
DEVICE_ID = "pico-serverroom-01"

# thresholds for the server room
TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60
SLEEP_TIME = 3

# connect_wifi waits two seconds per try, so this is 90 seconds of patience
WIFI_PATIENCE = 45


def get_status(temperature, humidity):
    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        return "ALARM"
    return "OK"


def show_status(status, seconds):
    # we only have one led, so it shines when everything is ok and blinks
    # when there is an alarm. it also does the waiting between the readings
    if status == "OK":
        status_led.value(1)
        time.sleep(seconds)
    else:
        for _ in range(int(seconds * 4)):
            status_led.toggle()
            time.sleep(.25)
        status_led.value(0)


def blink_while_waiting(times):
    # fast blinking means that the pico is not connected yet
    for _ in range(times):
        status_led.toggle()
        time.sleep(.2)
    status_led.value(0)


def wait_for_wifi():
    # after the pico has been powered on the radio can need over a minute to
    # join. calling connect again too early restarts the whole handshake, so
    # we give it plenty of time before we try a new round
    while not connect_wifi(WIFI_PATIENCE):
        print("Wifi did not answer, trying again")
        blink_while_waiting(10)


def connect_mqtt():
    while True:
        try:
            client = MQTTClient(client_id=DEVICE_ID, server=MQTT_BROKER, port=1883)
            client.connect()
            print("Connected to MQTT")
            return client
        except OSError as error:
            # the broker might not be started yet
            print(f"Could not reach the broker: {error}, trying again")
            blink_while_waiting(10)
            wait_for_wifi()


status_led.value(0)

wait_for_wifi()
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
    except OSError as error:
        # the wifi or the broker disappeared, connect again and keep going
        print(f"Could not send: {error}, reconnecting")
        wait_for_wifi()
        client = connect_mqtt()
        continue

    show_status(status, SLEEP_TIME)
