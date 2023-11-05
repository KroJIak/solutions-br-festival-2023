from modules.arduino import Arduino
import modules.custom as ctm
import time

ctm.showConfirmToStart()

# МИНИМУМ 1430 !!!!!!!
CAR_SPEED = 1440
DELAY = 33

arduino = Arduino(ctm.ARDUINO_PORT, baudrate=115200, timeout=10)
time.sleep(2)
arduino.set_angle(90)   # Первое сообщение подается, чтобы очистить буфер обмена,
time.sleep(0.05)                # оно не принимается микроконтроллером

try:
    arduino.set_speed(CAR_SPEED)
    while True:
        for angle in [70, 110]:
            arduino.set_angle(angle)
            time.sleep(DELAY)
except KeyboardInterrupt as err:
    print(f'[WARN] Program want to stop! {err} \n')
    print('[INFO] Отключи питание моторов!!!!')

ctm.showConfirmToStop()

arduino.stop()
arduino.set_angle(90)
