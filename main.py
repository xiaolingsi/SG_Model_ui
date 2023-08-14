from flask import render_template, jsonify
from model.model import app, WeatherStation, Lwm2m, ColdWaterMachine
import numpy as np
from datetime import datetime, timedelta


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
    return jsonify(time=time_, temperature=temperature, maxtemp=max_, mintemp=min_)


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

    return jsonify(time= list(time_new), temperature= list(averages_new))


@app.route('/home/cold_cpu')
def cold_water_api():
    # 冷水主机两小时数据，每2分钟一次，5个主机一小时150，两小时300
    cold_data = ColdWaterMachine.query.order_by(ColdWaterMachine.id.desc()).limit(300)
    time_ = []
    data_dict = {}
    for i in range(5):
        data_dict["in_temperature_" + str(i)] = []
        data_dict["out_temperature_" + str(i)] = []
    for ele in cold_data:
        for i in range(5):
            if ele.device_id == 'reju' + str(i):
                time_.append(ele.Update_time)
                data_dict["in_temperature_" + str(i)].append(ele.Cwpt)
                data_dict["out_temperature_" + str(i)].append(
                    min(ele.CrT, ele.CsT, ele.Eat, ele.AhoT, ele.AhsT, ele.CpaTime))
    # 指定时间间隔
    time_gap = 30
    data_count = int(3600 * 2 / time_gap)
    for key, value in data_dict:
        averages = value
        averages.reverse()

        x_sticks = [i * data_count / len(averages) for i in range(len(averages))]
        x = np.array([i for i in range(data_count)])
        averages_new = np.interp(x, x_sticks, averages)
        data_dict[key] = averages_new

    time_format = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(time_[-1], time_format)
    end_time = datetime.strptime(time_[0], time_format)
    time_interval = (end_time - start_time) / data_count

    # 生成均分的时间戳
    time_stamps = [start_time + i * time_interval for i in range(data_count + 1)]

    # 移除最后一个时间戳
    time_stamps.pop()

    time_new = time_stamps

    return jsonify(time=time_new, temperature=data_dict)


if __name__ == '__main__':
    app.run()
