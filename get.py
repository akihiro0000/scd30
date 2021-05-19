from scd30_i2c import SCD30
import time
import paho.mqtt.client as mqtt
import pytz
from datetime import datetime

scd30 = SCD30()

scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

time.sleep(2)

t0 = time.time()
mqtt_client = mqtt.Client()
mqtt_client.connect("fluent-bit",1883, 60)
while True:
    if scd30.get_data_ready():
        if (time.time() - t0)>10 :
            m = scd30.read_measurement()
            if m is not None:
                tim = '"timestamp":"'+datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S.%f')+'"'
                temp = '"' + "temp(degree)" + '"' + ":" + '"' + str(round(m[1],3)) + '"'
                hum = '"' + "humid(%)" + '"' + ":" + '"' + str(round(m[2],3)) + '"'
                co2 = '"' + "humid(%)" + '"' + ":" + '"' + str(round(m[0],3)) + '"'
                mylist = [tim,temp,hum,co2]
                mystr = '{' + ','.join(map(str,mylist))+'}'
                print(mystr)
                mqtt_client.publish("{}/{}".format("/demo",'car_count'), mystr)
                time.sleep(2)
            t0 = time.time()
    else:
        time.sleep(0.2)
mqtt_client.disconnect()
