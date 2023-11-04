import time
import serial

from arduino import Arduino
from utils import *


ARDUINO_PORT = '/dev/ttyUSB0'

arduino = Arduino(ARDUINO_PORT, baudrate=115200, timeout=10)
time.sleep(2)
arduino.set_angle(90) # Первое сообщение для очистки буфера обмена

print("Start")

# Командой set_speed мы задаем скорость беспилотника
# Значение 1500 означает остановку Айкара
# Для движение вперед используются значения в пределах 1415-1450 (чем меньше значение, тем больше скорость)
# Командой set_angle мы задаем угол поворота колес беспилотника
# Значение 90 выставляет колеса прямо
# Для поворота колес используются значение в пределах 70-110 (70 - крайнее правое значение. 110 - крайнее левое значение)

# ЗАПРЕЩАЕТСЯ ВЫХОДИТЬ ЗА ПРЕДЕЛЫ УСТАНОВЛЕННЫХ ЗНАЧЕНИЙ

arduino.set_angle(110)
arduino.set_speed(1430)
time.sleep(5)

arduino.set_angle(90)
arduino.set_speed(1500)

print("End")
