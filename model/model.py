# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus as urlquote


app = Flask(__name__,template_folder="../templates/")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://admin:{urlquote("reju@20220601!")}@{"180.76.100.226"}:3306/lwm?connect_timeout=300'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
db = SQLAlchemy(app)
Base = db.Model
metadata = Base.metadata



t_ammeter = Table(
    'ammeter', metadata,
    Column('local_time', String(50)),
    Column('tp', String(20)),
    Column('ammeter_id', String(15), info='设备编号'),
    Column('ax_v', Float(asdecimal=True), info='A相电压'),
    Column('bx_v', Float(asdecimal=True), info='B相电压'),
    Column('cx_v', Float(asdecimal=True), info='C相电压'),
    Column('ab_wire_v', Float(asdecimal=True), info='AB线电压'),
    Column('bc_wire_v', Float(asdecimal=True), info='BC线电压'),
    Column('ca_wire_v', Float(asdecimal=True), info='CA线电压'),
    Column('ax_a2', Float(asdecimal=True), info='A相电流'),
    Column('bx_a2', Float(asdecimal=True), info='B相电流'),
    Column('cx_a2', Float(asdecimal=True), info='C相电流'),
    Column('ax_kw', Float(asdecimal=True), info='A相有功功率'),
    Column('bx_kw', Float(asdecimal=True), info='B相有功功率'),
    Column('cx_kw', Float(asdecimal=True), info='C相有功功率'),
    Column('total_active_kw', Float(asdecimal=True), info='总有功功率'),
    Column('ax_kvar', Float(asdecimal=True), info='A相无功功率'),
    Column('bx_kvar', Float(asdecimal=True), info='B相无功功率'),
    Column('cx_kvar', Float(asdecimal=True), info='C相无功功率'),
    Column('total_reactive_kvar', Float(asdecimal=True), info='总无功功率'),
    Column('ax_kva', Float(asdecimal=True), info='A相视在功率'),
    Column('bx_kva', Float(asdecimal=True), info='B相视在功率'),
    Column('cx_kva', Float(asdecimal=True), info='C相视在功率'),
    Column('total_apparent_power', Float(asdecimal=True), info='总视在功率'),
    Column('ax_power_factor', Float(asdecimal=True), info='A相功率因数'),
    Column('bx_power_factor', Float(asdecimal=True), info='B相功率因数'),
    Column('cx_power_factor', Float(asdecimal=True), info='C相功率因数'),
    Column('overall_power_factor', Float(asdecimal=True), info='总功率因数'),
    Column('hz', Integer, info='频率'),
    Column('dbm', Integer, info='信号强度'),
    Column('front_kwh', Float(asdecimal=True), info='正向有功总电能示值'),
    Column('reverse_kwh', Integer, info='反向有功总电能示值'),
    Column('front_kvarh', Float(asdecimal=True), info='正向无功总电能示值'),
    Column('reverse_kvarh', Integer, info='反向无功总电能示值'),
    Column('now_demand_kw', Float(asdecimal=True), info='当前有功需量'),
    Column('iccid', String(30, 'utf8mb4_0900_ai_ci'), info='工况'),
    Column('pt', Integer, info='电压变比'),
    Column('ct', Integer, info='电流'),
    Column('ax_t', Integer, info='A相温度'),
    Column('bx_t', Integer, info='B相温度'),
    Column('cx_t', Integer, info='C相温度'),
    Column('nx_t', Integer, info='N相温度'),
    Column('aftercurrent_a', Integer, info='剩余电流'),
    Column('four_road_di', Integer, info='4路DI状态 ,bit0:DI1 bit1:DI2'),
    Column('ax_front_kwh', Float(asdecimal=True), info='A相正向有功总电能示值'),
    Column('ax_reverse_kwh', Integer, info='A相反向有功总电能示值'),
    Column('ax_front_kvarh', Float(asdecimal=True), info='A相正向无功总电能示值'),
    Column('ax_reverse_kvarh', Integer, info='A相反向无功总电能示值'),
    Column('bx_front_kwh', Float(asdecimal=True), info='B相正向有功总电能示值'),
    Column('bx_reverse_kwh', Integer, info='B相反向有功总电能示值'),
    Column('bx_front_kvarh', Float(asdecimal=True), info='B相正向无功总电能示值'),
    Column('bx_reverse_kvarh', Integer, info='B相反向无功总电能示值'),
    Column('cx_front_kwh', Float(asdecimal=True), info='C相正向有功总电能示值'),
    Column('cx_reverse_kwh', Integer, info='C相反向有功总电能示值'),
    Column('cx_front_kvarh', Float(asdecimal=True), info='C相正向无功总电能示值'),
    Column('cx_reverse_kvarh', Integer, info='C相反向无功总电能示值'),
    Column('ax_v_variation', Integer, info='A相谐波电压总畸变率'),
    Column('bx_v_variation', Integer, info='B相谐波电压总畸变率'),
    Column('cx_v_variation', Integer, info='C相谐波电压总畸变率'),
    Column('ax_a_variation', Float(asdecimal=True), info='A相谐波电流总畸变率'),
    Column('bx_a_variation', Float(asdecimal=True), info='B相谐波电流总畸变率'),
    Column('cx_a_variation', Float(asdecimal=True), info='C相谐波电流总畸变率'),
    Column('now_reverse_kw', Integer, info='当前反向有功需量'),
    Column('now_front_kvar', Float(asdecimal=True), info='当前正向无功需量'),
    Column('now_reverse_kvar', Integer, info='当前反向无功需量'),
    Column('v_imbalance', Float(asdecimal=True), info='电压不平衡度'),
    Column('a_imbalance', Float(asdecimal=True), info='电流不平衡度'),
    Column('full_power_kwh', Integer, info='尖时段有功总电能'),
    Column('peak_power_kwh', Integer, info='峰时段有功总电能'),
    Column('pacific_power_kwh', Integer, info='平时段有功总电能'),
    Column('low_power_kwh', Integer, info='谷时段有功总电能'),
    Column('first_quartile_kvarh', Integer, info='第一象限无功电能'),
    Column('second_quartile_kvarh', Integer, info='第二象限无功电能'),
    Column('thire_quartile_kvarh', Integer, info='第三象限无功电能'),
    Column('four_quartile_kvarh', Integer, info='第四象限无功电能')
)



t_ammeter_copy = Table(
    'ammeter_copy', metadata,
    Column('local_time', String(50)),
    Column('tp', String(20)),
    Column('ammeter_id', String(15), info='设备编号'),
    Column('ax_v', Float(asdecimal=True), info='A相电压'),
    Column('bx_v', Float(asdecimal=True), info='B相电压'),
    Column('cx_v', Float(asdecimal=True), info='C相电压'),
    Column('ab_wire_v', Float(asdecimal=True), info='AB线电压'),
    Column('bc_wire_v', Float(asdecimal=True), info='BC线电压'),
    Column('ca_wire_v', Float(asdecimal=True), info='CA线电压'),
    Column('ax_a2', Float(asdecimal=True), info='A相电流'),
    Column('bx_a2', Float(asdecimal=True), info='B相电流'),
    Column('cx_a2', Float(asdecimal=True), info='C相电流'),
    Column('ax_kw', Float(asdecimal=True), info='A相有功功率'),
    Column('bx_kw', Float(asdecimal=True), info='B相有功功率'),
    Column('cx_kw', Float(asdecimal=True), info='C相有功功率'),
    Column('total_active_kw', Float(asdecimal=True), info='总有功功率'),
    Column('ax_kvar', Float(asdecimal=True), info='A相无功功率'),
    Column('bx_kvar', Float(asdecimal=True), info='B相无功功率'),
    Column('cx_kvar', Float(asdecimal=True), info='C相无功功率'),
    Column('total_reactive_kvar', Float(asdecimal=True), info='总无功功率'),
    Column('ax_kva', Float(asdecimal=True), info='A相视在功率'),
    Column('bx_kva', Float(asdecimal=True), info='B相视在功率'),
    Column('cx_kva', Float(asdecimal=True), info='C相视在功率'),
    Column('total_apparent_power', Float(asdecimal=True), info='总视在功率'),
    Column('ax_power_factor', Float(asdecimal=True), info='A相功率因数'),
    Column('bx_power_factor', Float(asdecimal=True), info='B相功率因数'),
    Column('cx_power_factor', Float(asdecimal=True), info='C相功率因数'),
    Column('overall_power_factor', Float(asdecimal=True), info='总功率因数'),
    Column('hz', Integer, info='频率'),
    Column('dbm', Integer, info='信号强度'),
    Column('front_kwh', Float(asdecimal=True), info='正向有功总电能示值'),
    Column('reverse_kwh', Integer, info='反向有功总电能示值'),
    Column('front_kvarh', Float(asdecimal=True), info='正向无功总电能示值'),
    Column('reverse_kvarh', Integer, info='反向无功总电能示值'),
    Column('now_demand_kw', Float(asdecimal=True), info='当前有功需量'),
    Column('iccid', String(30, 'utf8mb4_0900_ai_ci'), info='工况'),
    Column('pt', Integer, info='电压变比'),
    Column('ct', Integer, info='电流'),
    Column('ax_t', Integer, info='A相温度'),
    Column('bx_t', Integer, info='B相温度'),
    Column('cx_t', Integer, info='C相温度'),
    Column('nx_t', Integer, info='N相温度'),
    Column('aftercurrent_a', Integer, info='剩余电流'),
    Column('four_road_di', Integer, info='4路DI状态 ,bit0:DI1 bit1:DI2'),
    Column('ax_front_kwh', Float(asdecimal=True), info='A相正向有功总电能示值'),
    Column('ax_reverse_kwh', Integer, info='A相反向有功总电能示值'),
    Column('ax_front_kvarh', Float(asdecimal=True), info='A相正向无功总电能示值'),
    Column('ax_reverse_kvarh', Integer, info='A相反向无功总电能示值'),
    Column('bx_front_kwh', Float(asdecimal=True), info='B相正向有功总电能示值'),
    Column('bx_reverse_kwh', Integer, info='B相反向有功总电能示值'),
    Column('bx_front_kvarh', Float(asdecimal=True), info='B相正向无功总电能示值'),
    Column('bx_reverse_kvarh', Integer, info='B相反向无功总电能示值'),
    Column('cx_front_kwh', Float(asdecimal=True), info='C相正向有功总电能示值'),
    Column('cx_reverse_kwh', Integer, info='C相反向有功总电能示值'),
    Column('cx_front_kvarh', Float(asdecimal=True), info='C相正向无功总电能示值'),
    Column('cx_reverse_kvarh', Integer, info='C相反向无功总电能示值'),
    Column('ax_v_variation', Integer, info='A相谐波电压总畸变率'),
    Column('bx_v_variation', Integer, info='B相谐波电压总畸变率'),
    Column('cx_v_variation', Integer, info='C相谐波电压总畸变率'),
    Column('ax_a_variation', Float(asdecimal=True), info='A相谐波电流总畸变率'),
    Column('bx_a_variation', Float(asdecimal=True), info='B相谐波电流总畸变率'),
    Column('cx_a_variation', Float(asdecimal=True), info='C相谐波电流总畸变率'),
    Column('now_reverse_kw', Integer, info='当前反向有功需量'),
    Column('now_front_kvar', Float(asdecimal=True), info='当前正向无功需量'),
    Column('now_reverse_kvar', Integer, info='当前反向无功需量'),
    Column('v_imbalance', Float(asdecimal=True), info='电压不平衡度'),
    Column('a_imbalance', Float(asdecimal=True), info='电流不平衡度'),
    Column('full_power_kwh', Integer, info='尖时段有功总电能'),
    Column('peak_power_kwh', Integer, info='峰时段有功总电能'),
    Column('pacific_power_kwh', Integer, info='平时段有功总电能'),
    Column('low_power_kwh', Integer, info='谷时段有功总电能'),
    Column('first_quartile_kvarh', Integer, info='第一象限无功电能'),
    Column('second_quartile_kvarh', Integer, info='第二象限无功电能'),
    Column('thire_quartile_kvarh', Integer, info='第三象限无功电能'),
    Column('four_quartile_kvarh', Integer, info='第四象限无功电能')
)



class ColdWaterMachine(Base):
    __tablename__ = 'cold_water_machine'

    id = Column(BigInteger, primary_key=True)
    start = Column(Integer)
    model = Column(Integer)
    CrsT = Column(Float)
    HrsT = Column(Float)
    AhoT = Column(Float)
    AhsT = Column(Float)
    IwTP = Column(Float)
    CpaTime = Column(Integer)
    Cwpt = Column(Float)
    CrT = Column(Float)
    CsT = Column(Float)
    EaT = Column(Float)
    Alm1 = Column(Float)
    Alm2 = Column(Integer)
    DRime = Column(Integer)
    qAlm = Column(Integer)
    device_id = Column(String(10))
    Update_time = Column(String(50))



class ColdWaterMachineCopy(Base):
    __tablename__ = 'cold_water_machine_copy'

    id = Column(BigInteger, primary_key=True)
    start = Column(Integer)
    model = Column(Integer)
    CrsT = Column(Float)
    HrsT = Column(Float)
    AhoT = Column(Float)
    AhsT = Column(Float)
    IwTP = Column(Float)
    CpaTime = Column(Integer)
    Cwpt = Column(Float)
    CrT = Column(Float)
    CsT = Column(Float)
    EaT = Column(Float)
    Alm1 = Column(Float)
    Alm2 = Column(Integer)
    DRime = Column(Integer)
    qAlm = Column(Integer)
    device_id = Column(String(10))
    Update_time = Column(DateTime)



class Controlpanel(Base):
    __tablename__ = 'controlpanel'

    id = Column(BigInteger, primary_key=True)
    panelid = Column(String(30, 'utf8mb4_0900_ai_ci'))
    dpf2_sheT = Column(Integer)
    dpf2_start = Column(Integer)
    dpf2_sheF = Column(Integer)
    dpf3_sheT = Column(Integer)
    dpf3_start = Column(Integer)
    dpf3_sheF = Column(Integer)
    dpf4_sheT = Column(Integer)
    dpf4_start = Column(Integer)
    dpf4_sheF = Column(Integer)
    dpf5_sheT = Column(Integer)
    dpf5_start = Column(Integer)
    dpf5_sheF = Column(Integer)
    dpf6_sheT = Column(Integer)
    dpf6_start = Column(Integer)
    dpf6_sheF = Column(Integer)
    ctime = Column(String(30))



class Lwm2m(Base):
    __tablename__ = 'lwm2m'

    ID = Column(BigInteger, primary_key=True)
    D_ID = Column(String(8, 'utf8mb4_0900_ai_ci'), info='设备SN，8位出厂唯一编码')
    D_WORKSTATION = Column(Integer, info='1.上电重启 2.业务数据 3.低电压关机 4.紧急事件 5. WDT重启 6.软重启 7.RST重启 8.其他 9.传感器故障')
    D_IMEI = Column(String(20, 'utf8mb4_0900_ai_ci'), info='IMEI号码')
    D_RSSI = Column(Integer, info='99表示无信号，31表示信号最强')
    NB_CARDNM = Column(String(20, 'utf8mb4_0900_ai_ci'), info='NB卡号')
    TEMP_COMP = Column(Integer, info='代表-12.8℃到12.7℃之间')
    DATACOL_INTERVAL = Column(Integer, info='1-60代表1-60分钟，101-160代表1-60小时，默认60')
    D_POWER = Column(String(8, 'utf8mb4_0900_ai_ci'), info='0代表断电，1代表通电')
    DATA_TEMP = Column(Float(asdecimal=True), info='采集当前温度')
    DATACOL_DATATIME = Column(String(22, 'utf8mb4_0900_ai_ci'), info='温度及设备状态货期时间，有8小时时差，已调整')



class Lwm2mCopy(Base):
    __tablename__ = 'lwm2m_copy'

    ID = Column(BigInteger, primary_key=True)
    D_ID = Column(String(8), info='设备SN，8位出厂唯一编码')
    D_WORKSTATION = Column(Integer, info='1.上电重启 2.业务数据 3.低电压关机 4.紧急事件 5. WDT重启 6.软重启 7.RST重启 8.其他 9.传感器故障')
    D_IMEI = Column(String(20), info='IMEI号码')
    D_RSSI = Column(Integer, info='99表示无信号，31表示信号最强')
    NB_CARDNM = Column(String(20), info='NB卡号')
    TEMP_COMP = Column(Integer, info='代表-12.8℃到12.7℃之间')
    DATACOL_INTERVAL = Column(Integer, info='1-60代表1-60分钟，101-160代表1-60小时，默认60')
    D_POWER = Column(String(8), info='0代表断电，1代表通电')
    DATA_TEMP = Column(Float(asdecimal=True), info='采集当前温度')
    DATACOL_DATATIME = Column(String(22), info='温度及设备状态货期时间，有8小时时差，已调整')



class NoSmartDate(Base):
    __tablename__ = 'no_smart_date'

    id = Column(BigInteger, primary_key=True)
    NoSmart_date = Column(String(50))



t_operation_log = Table(
    'operation_log', metadata,
    Column('Operation_time', String(20)),
    Column('device', String(20)),
    Column('key', String(20)),
    Column('value', String(20))
)



t_position_temp = Table(
    'position_temp', metadata,
    Column('D_ID', String(255, 'utf8mb4_0900_ai_ci')),
    Column('Position', String(255)),
    Column('place', String(10))
)



t_power_predict = Table(
    'power_predict', metadata,
    Column('P_time', String(20)),
    Column('mz_power', Float(30, True)),
    Column('women_power', Float(30, True)),
    Column('child_power', Float(30, True))
)



t_predict_res = Table(
    'predict_res', metadata,
    Column('Pre_Time', String(50)),
    Column('Temp_predict', Float(asdecimal=True)),
    Column('Humi_predict', Float(asdecimal=True))
)



class TempModify(Base):
    __tablename__ = 'temp_modify'

    id = Column(BigInteger, primary_key=True)
    modify_date = Column(String(20))
    inside_modify_temp = Column(Float)
    outside_modify_temp = Column(Float)



t_user = Table(
    'user', metadata,
    Column('Id', Integer),
    Column('Username', String(255)),
    Column('Password', String(255))
)



class WeatherStation(Base):
    __tablename__ = 'weather_stations'

    lOC_TIME = Column(String(30, 'utf8mb4_0900_ai_ci'), primary_key=True, info='时间')
    TEMPERATURE = Column(Float, info='温度')
    HUMIDITY = Column(Float, info='湿度')
    WIND_DIR = Column(Float, info='风速')
    WIND_SPEED = Column(Float, info='风向')
    SUN_SHINE = Column(BigInteger, info='日照')



t_weather_stations_copy = Table(
    'weather_stations_copy', metadata,
    Column('lOC_TIME', DateTime, info='时间'),
    Column('TEMPERATURE', Float, info='温度'),
    Column('HUMIDITY', Float, info='湿度'),
    Column('WIND_DIR', Float, info='风速'),
    Column('WIND_SPEED', Float, info='风向'),
    Column('SUN_SHINE', BigInteger, info='日照')
)
