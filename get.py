from scd30_i2c import SCD30
import time
import paho.mqtt.client as mqtt
import pytz
from datetime import datetime
import os

try:
    scd30 = SCD30()

    scd30.set_measurement_interval(10)
    scd30.start_periodic_measurement()

    time.sleep(2)
except TimeoutError as e:
    print(e)
    os.system('ls')
    pass


mqtt_client = mqtt.Client()
mqtt_client.connect("fluent-bit",1883, 60)
while True:
    try:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            if m is not None:
                tim = '"timestamp":"'+datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S.%f')+'"'
                temp = '"' + "temp(degree)" + '"' + ":" + '"' + str(round(m[1],3)) + '"'
                hum = '"' + "humid(%)" + '"' + ":" + '"' + str(round(m[2],3)) + '"'
                co2 = '"' + "co2(ppm)" + '"' + ":" + '"' + str(round(m[0],3)) + '"'
                mylist = [tim,temp,hum,co2]
                mystr = '{' + ','.join(map(str,mylist))+'}'
                if str(round(m[1],3))!="nan":
                    print(mystr)
                    mqtt_client.publish("{}/{}".format("/demo",'car_count'), mystr)
                    time.sleep(1)
                else:
                    print("value is nan")
                    time.sleep(1)
        else:
            time.sleep(0.2)
    except OSError as e:
        print(e)
        pass
mqtt_client.disconnect()
