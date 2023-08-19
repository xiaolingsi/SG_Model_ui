import queue
from threading import Thread

import paho.mqtt.client as mqtt

from MQTT_info.SG_mqtt_info import on_connect, on_message, clear_old_messages

def mqtt_collect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("180.76.100.226", 1883, 60)
    client.loop_start()

thread_process = Thread(target=mqtt_collect())
thread_process.daemon = True
thread_process.start()
# 创建并启动清除消息的线程
clear_thread = Thread(target=clear_old_messages)
clear_thread.daemon = True
clear_thread.start()