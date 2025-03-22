import wmi
import os
import time



def lanceopen():
    path = os.path.dirname(os.path.abspath(__file__))
    print(path+"\OpenHardware\OpenHardwareMonitor.exe")
    os.startfile(path+"\OpenHardware\OpenHardwareMonitor.exe")

def getTtemp(name):
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature' and sensor.Name ==name:
            return sensor.Value
