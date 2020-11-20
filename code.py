print('Hello World!')

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio 
import terminalio
from adafruit_display_text import label
import adafruit_il0373
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import busio
import adafruit_bme680 
import adafruit_sgp30
from adafruit_display_shapes.rect import Rect
import adafruit_imageload

i2c = busio.I2C(board.SCL, board.SDA)
bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

print('Temperature: {} degrees C'.format(bme680_sensor.temperature))
print('Gas: {} ohms'.format(bme680_sensor.gas))
print('Humidity: {}%'.format(bme680_sensor.humidity))
print('Pressure: {}hPa'.format(bme680_sensor.pressure))

sgp30_sensor = adafruit_sgp30.Adafruit_SGP30(i2c)
print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30_sensor.eCO2, sgp30_sensor.TVOC))

display = board.DISPLAY

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
led.value = True

splash = displayio.Group(max_size=20)
# background
rect = Rect(0, 0, 296, 128, fill=0xFFFFFF)
# Text
font = bitmap_font.load_font("/Exo-Bold-75.bdf")
color = 0x000000
text = "{:4.2f}°".format(bme680_sensor.temperature)
text_area1 = label.Label(font, text=text, color=color)
text_area1.x = 28
text_area1.y = 40
text_area1.background_color=0xFFFFFF
## Bitmaps
thermometer_bitmap = displayio.OnDiskBitmap(open("/thermometer.bmp", "rb"))
tilegrid = displayio.TileGrid(thermometer_bitmap, pixel_shader=displayio.ColorConverter())
tilegrid.x = 10
tilegrid.y = 10

splash.append(rect)
splash.append(text_area1)
splash.append(tilegrid)

display.show(splash)
print("WTF")
display.refresh()
print("WTF")
elapsed_sec = 0

while True:
    time.sleep(1)
    elapsed_sec += 1
    if elapsed_sec > 5 * 60:
        print("========================")
        print('BME Temperature: {} C'.format(bme680_sensor.temperature))
        print('BME Gas: {} ohms'.format(bme680_sensor.gas))
        print('BME Humidity: {}%'.format(bme680_sensor.humidity))
        print('BME Pressure: {}hPa'.format(bme680_sensor.pressure))

        print("SGP eCO2 = %d ppm" % (sgp30_sensor.eCO2))
        print("SGP TVOC = %d ppb" % (sgp30_sensor.TVOC))

        elapsed_sec = 0
        text_area1.text = "{:4.2f}°".format(bme680_sensor.temperature)
        display.show(splash)
        display.refresh()
