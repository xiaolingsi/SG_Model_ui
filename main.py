import json
import time
import random
from MQTT_info import *
import torch
from flask import render_template, jsonify
from sklearn.linear_model import LinearRegression

from MLmodel.temperature_predict import GRUModel
from MQTT_info.SG_mqtt_info import message_queue
from model.model import app, WeatherStation, Lwm2m, ColdWaterMachine
import numpy as np
from datetime import datetime, timedelta
out_temperature = []
in_temperature = []
first_out_flag = True
first_in_flag = True

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/home/temperature')
def temperature_api():
    # 气象站每分钟2条记录，一小时120，两小时240条数据
    weather_data = WeatherStation.query.order_by(WeatherStation.lOC_TIME.desc()).limit(240)
    time_ = []
    temperature = []
    max_ = -99
    min_ = 99
    for ele in weather_data:
        time_.append(ele.lOC_TIME)
        temperature.append(ele.TEMPERATURE)
        if ele.TEMPERATURE > max_: max_ = ele.TEMPERATURE
        if ele.TEMPERATURE < min_: min_ = ele.TEMPERATURE
    time_.reverse()
    temperature.reverse()
    if first_out_flag:
        global out_temperature
        out_temperature = temperature
    return jsonify(time=time_, temperature=temperature, maxtemp=max_, mintemp=min_)


@app.route('/home/temperature_pre')
def temperature_predict():
    time.sleep(.5)
    global out_temperature
    past_temperatures = out_temperature
    # 获取当前时间
    current_time = datetime.now()
    timestamps = []
    for i in range(-7200, 1, 30):  # 2小时，每30秒一个数据点
        timestamp = current_time + timedelta(seconds=i)
        timestamps.append(timestamp)

    # 使用过去的温度数据载入神经网络预测
    temp_input = past_temperatures[-150:]
    temp_input = np.array([(ele - 2.8) / (41.9 - 2.8) for ele in temp_input])
    temp_input =  torch.tensor(temp_input.reshape((1,-1,1)),dtype=torch.float32)
    # temp_input = temp_input.to(torch.float32)
    # 创建一个新的模型实例
    loaded_model = GRUModel(1, 64, 2, 40)
    # 加载训练好的模型参数
    loaded_model.load_state_dict(torch.load('/Users/zkx/Documents/PythonProject/SG_Model_ui/MLmodel/gru_temp_model.pth'))

    # 设置模型为评估模式
    loaded_model.eval()

    # 在其他地方使用模型进行预测
    with torch.no_grad():
        # 使用模型进行预测
        predictions = loaded_model(temp_input)
    future_temperatures = np.array(predictions).reshape(-1,1)
    future_temperatures = [ele * (41.9 - 2.8)+ 2.8 for ele in future_temperatures]
    # 生成未来20分钟的时间戳列表
    future_timestamps = []
    for i in range(1, 1201, 30):  # 20分钟，每30秒一个数据点
        timestamp = current_time + timedelta(seconds=i)
        future_timestamps.append(timestamp)

    timestamps.extend(future_timestamps)
    past_temperatures.extend(list(np.array(future_temperatures,dtype=float).reshape((1,-1))[0]))
    return jsonify(time=timestamps, temperature=list(past_temperatures))

@app.route('/home/inside_temp')
def inside_temp_api():
    # 室内温度采集器，30分钟上传一次，一共38个，一小时76条数据，取两小时160条数据
    inside_data = Lwm2m.query.order_by(Lwm2m.ID.desc()).limit(160)
    time_ = []
    temperature = []

    for ele in inside_data:
        time_.append(ele.DATACOL_DATATIME)
        temperature.append(ele.DATA_TEMP)
    group_size = 40
    averages = [float(sum(temperature[i:i + group_size]) / group_size ) for i in range(0, len(temperature), group_size)]
    averages.reverse()

    # 指定时间间隔
    time_gap = 10
    data_count = int(3600 * 2 / time_gap)
    x_sticks = [i * data_count / len(averages) for i in range(len(averages))]
    x = [i + 1 for i in range(data_count)]
    averages_new = np.interp(x, x_sticks, averages)

    time_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(time_[-1], time_format)
    end_time = datetime.strptime(time_[0], time_format)
    time_interval = (end_time - start_time) / data_count

    # 生成均分的时间戳
    time_stamps = [start_time + i * time_interval for i in range(data_count + 1)]

    # 移除最后一个时间戳
    time_stamps.pop()
    time_new = time_stamps
    if first_in_flag:
        global in_temperature
        in_temperature = averages_new
    return jsonify(time= list(time_new), temperature= list(averages_new))


@app.route('/home/insidetemp_pre')
def inside_temp_predict():
    time.sleep(.5)
    global in_temperature
    past_temperatures = list(in_temperature)
    # 获取当前时间
    current_time = datetime.now()
    timestamps = []
    for i in range(-7200, 1, 30):  # 2小时，每30秒一个数据点
        timestamp = current_time + timedelta(seconds=i)
        timestamps.append(timestamp)
    future_temperatures = [ele + random.uniform(-.1,.1) for ele in past_temperatures[-40:]]
    # 生成未来20分钟的时间戳列表
    future_timestamps = []
    for i in range(1, 1201, 30):  # 20分钟，每30秒一个数据点
        timestamp = current_time + timedelta(seconds=i)
        future_timestamps.append(timestamp)

    timestamps.extend(future_timestamps)
    past_temperatures.extend(list(np.array(future_temperatures,dtype=float).reshape((1,-1))[0]))
    return jsonify(time=timestamps, temperature=list(past_temperatures))


@app.route('/home/cold_cpu')
def cold_water_api():
    # 冷水主机两小时数据，每2分钟一次，5个主机一小时150，两小时300
    cold_data = ColdWaterMachine.query.order_by(ColdWaterMachine.id.desc()).limit(300)
    time_ = []
    data_dict = {}
    for i in range(1,6):
        data_dict["in_temperature_" + str(i)] = []
        data_dict["out_temperature_" + str(i)] = []
    for ele in cold_data:
        for i in range(1,6):
            if ele.device_id == 'reju' + str(i):
                time_.append(ele.Update_time)
                data_dict["in_temperature_" + str(i)].append(ele.Cwpt/10)
                data_dict["out_temperature_" + str(i)].append(
                    min(ele.CrT, ele.CsT, ele.EaT, ele.AhoT, ele.AhsT, ele.CpaTime)/10)
    # 指定时间间隔
    time_gap = 30
    data_count = int(3600 * 2 / time_gap)
    for key, value in data_dict.items():
        averages = value
        averages.reverse()
        x_sticks = [i * data_count / len(averages) for i in range(len(averages))]
        x = np.array([i for i in range(data_count)])
        averages_new = np.interp(x, x_sticks, averages)
        data_dict[key] = list(averages_new)

    time_format = "%Y/%m/%d %H:%M:%S"
    start_time = datetime.strptime(time_[-1], time_format)
    end_time = datetime.strptime(time_[0], time_format)
    time_interval = (end_time - start_time) / data_count

    # 生成均分的时间戳
    time_stamps = [start_time + i * time_interval for i in range(data_count + 1)]

    # 移除最后一个时间戳
    time_stamps.pop()

    time_new = time_stamps

    return jsonify(time=list(time_new), temperature= data_dict)


@app.route("/home/info")
def mqtt_info():
    message_queue.put((datetime.now(), 123))
    message_queue.put((datetime.now(), 123))
    message_queue.put((datetime.now(), 123))
    res = message_queue.queue
    return list(res)


if __name__ == '__main__':
    app.run(port=8888)
