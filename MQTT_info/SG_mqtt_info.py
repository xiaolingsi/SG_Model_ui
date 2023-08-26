import json
import queue
import random
import time
from datetime import datetime,timedelta
import paho.mqtt.client as mqtt
from threading import Thread
message_queue = queue.Queue()
position_map = {
    '1':'妇产楼',
    '2':'儿童楼',
    '4':'门诊楼1',
    '5':'门诊楼2'
}
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
    message = json.loads(msg.payload.decode())
    print(message)
    position = position_map.get(message.get('Pid'))
    temp = float(message.get('Addrv'))/10
    message = '设定 '+position+' 主机回水温度: '+ str(temp) + "°C"
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    message_queue.put((formatted_time, message))
    if datetime.now().second.real % 3 == 1:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        message_queue.put((formatted_time, position + '水泵阀门开度变更为：'+str(random.randint(40,80)) + '%'))

# 启动 MQTT 客户端


# 启动 Flask 的定时任务，每分钟清除超过10分钟的消息
def clear_old_messages():
    print("start clean message Thread")
    while True:
        current_time = datetime.now()
        while not message_queue.empty():
            timestamp, message = message_queue.queue[0]
            timestamp = datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
            if current_time - timestamp > timedelta(minutes=15):
                message_queue.get()
            else:
                break
        time.sleep(60)
