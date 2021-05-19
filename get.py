from scd30_i2c import SCD30
import time
import paho.mqtt.client as mqtt
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
                co2 = round(m[0],3)
                temp = round(m[1],3)
                humid = round(m[2],3)
                mylist = [tim,temp,hum,co2]
                mystr = '{' + ','.join(map(str,mylist))+'}'
                print(mystr)
                mqtt_client.publish("{}/{}".format("/demo",'car_count'), mystr)
                
                print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
            time.sleep(2)
        t0 = time.time()
    else:
        time.sleep(0.2)
mqtt_client.disconnect()
