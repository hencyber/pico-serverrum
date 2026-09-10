from machine import Pin
from dht import DHT11
import time

time.sleep(.5)

sensor = DHT11(Pin(16))
green_led = Pin(15, Pin.OUT)
red_led = Pin(14, Pin.OUT)

TEMP_LIMIT = 27
HUMIDITY_LIMIT = 60

while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    if temperature > TEMP_LIMIT or humidity > HUMIDITY_LIMIT:
        green_led.value(0)
        red_led.value(1)
    else:
        green_led.value(1)
        red_led.value(0)

    print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
    time.sleep(3)
