import os
import clr
import logging
logging.basicConfig(level=logging.INFO)
openhardwaremonitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU',
                               'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']

openhardwaremonitor_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load',
                                   'Fan', 'Flow', 'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData']


class CPUTemp:
    def __init__(self):
        if os.name == 'nt':
            file = 'CPUThermometerLib'
            clr.AddReference(file)
            from OpenHardwareMonitor import Hardware
            handle = Hardware.Computer()
            handle.CPUEnabled = True
            handle.Open()
            self.cpu = handle.Hardware[0]
            self.os = 1
            logging.debug("Win")
        else:
            import psutil
            self.os = 0

    def fetch_temp(self):
        self.cpu.Update()
        for sensor in (self.cpu.Sensors):
            # Temperature Type Index = 2
            # CPU Package Value, No need to Average out
            # if sensor.SensorType == 2:
            if sensor.Name == "CPU Package":
                return sensor.Value

    def get_win_cpu_temp(self):
        return self.fetch_temp()

    def get_linux_cpu_temp(self):
        pass

    def get_cpu_temp(self):
        if self.os == 1:
            return self.get_win_cpu_temp()
        else:
            return self.get_linux_cpu_temp()


C=CPUTemp()
print(C.get_cpu_temp())