import paho.mqtt.client as mqtt
import json
import os
import time
from utils.connect_postgres import query_db

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
TOPIC = "pico/serverroom/dht11"


def create_table():
    query_db("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            time TIMESTAMPTZ NOT NULL,
            device_id TEXT,
            temperature DOUBLE PRECISION,
            humidity DOUBLE PRECISION,
            status TEXT
        )
    """)
    # timescaledb wants a hypertable to be able to handle timeseries data fast
    query_db("""
        SELECT create_hypertable('sensor_readings', 'time', if_not_exists => TRUE)
    """)


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    device_id = data["device_id"]
    temperature = float(data["temperature"])
    humidity = float(data["humidity"])
    status = data["status"]

    query_db(
        """
        INSERT INTO sensor_readings
            (time, device_id, temperature, humidity, status)
        VALUES (NOW(), %s, %s, %s, %s)
""",
        (device_id, temperature, humidity, status),
    )

    print(f"saved: {device_id} {temperature}°C {humidity}% {status}")


if __name__ == "__main__":
    create_table()

    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883)
    client.subscribe(TOPIC)
    client.on_message = on_message
    print(f"Listening on topic {TOPIC}")
    client.loop_forever()
