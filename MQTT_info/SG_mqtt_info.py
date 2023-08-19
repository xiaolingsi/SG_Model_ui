import queue
import time
from datetime import datetime,timedelta
import paho.mqtt.client as mqtt
from threading import Thread
message_queue = queue.Queue()

# 连接到 MQTT 服务器的回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected MQTT server with result code "+str(rc))
    client.subscribe(topic = [('jie-gree1',0),
                              ('jie-gree2',0),
                              ('jie-gree3',0),
                              ('jie-gree4',0),
                              ('jie-gree5',0)])

# 接收到 MQTT 消息的回调函数
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(message)
    message_queue.put((datetime.now(), message))

# 启动 MQTT 客户端


# 启动 Flask 的定时任务，每分钟清除超过10分钟的消息
def clear_old_messages():
    print("start clean message Thread")
    while True:
        current_time = datetime.now()
        while not message_queue.empty():
            timestamp, message = message_queue.queue[0]
            if current_time - timestamp > timedelta(minutes=10):
                message_queue.get()
            else:
                break
        time.sleep(60)
