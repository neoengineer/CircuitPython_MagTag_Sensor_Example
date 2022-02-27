import time
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import terminalio
from adafruit_display_text import label
#import adafruit_il0373
from adafruit_bitmap_font import bitmap_font
import busio
#import adafruit_bme680
#import adafruit_sgp30
from adafruit_display_shapes.rect import Rect
import adafruit_imageload

from adafruit_dps310.advanced import DPS310_Advanced as DPS310

print('Setting up sensors')
i2c = busio.I2C(board.SCL, board.SDA)
#bme680_sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
#sgp30_sensor = adafruit_sgp30.Adafruit_SGP30(i2c)
dps310 = DPS310(i2c)

print('Setting up display')
display = board.DISPLAY

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
led.value = True

group = displayio.Group()
# background
rect1 = Rect(0, 0, 199, 90, fill=0xFFFFFF)
rect2 = Rect(200, 0, 296, 90, fill=0xBBBBBB)
rect3 = Rect(0, 91, 296, 128, fill=0x444444)

# Create fonts
print("Loading fonts")
big_font = bitmap_font.load_font("/Exo-Bold-42.bdf")
medium_font = bitmap_font.load_font("/Exo-SemiBold-18.bdf")
small_font = bitmap_font.load_font("/Exo-SemiBold-12.bdf")
tiny_font = bitmap_font.load_font("/Exo-SemiBold-6.bdf")

## Bitmaps
print("Loading bitmaps")
thermometer_bitmap = displayio.OnDiskBitmap(open("/thermometer.bmp", "rb"))
temperature_tile = displayio.TileGrid(thermometer_bitmap, pixel_shader=getattr(thermometer_bitmap, 'pixel_shader'), x=4, y=18)
humidity_bitmap = displayio.OnDiskBitmap(open("/water.bmp", "rb")) # "/water.bmp", "rb"))
humidity_tile = displayio.TileGrid(humidity_bitmap, pixel_shader=humidity_bitmap.pixel_shader, x=4, y=98)
pressure_bitmap = displayio.OnDiskBitmap(open("/cloud.bmp", "rb")) # "/cloud.bmp", "rb"))
#pressure_tile = displayio.TileGrid(pressure_bitmap, pixel_shader=pressure_bitmap.pixel_shader, x=115, y=92)
pressure_tile = displayio.TileGrid(pressure_bitmap, pixel_shader=pressure_bitmap.pixel_shader, x=130, y=98)

# Create sensor value labels
temperature_label = label.Label(big_font, text="123.4°", color=0x000000, x=28, y=45, background_color=0xFFFFFF)
temperature_label.anchor_point = (0.5, 0.5)
temperature_label.anchored_position = (100, 44)
humidity_label = label.Label(medium_font, text="12.34%", color=0xFFFFFF, x=30, y=110, background_color=0x444444)
pressure_label = label.Label(medium_font, text="1234hPa", color=0xFFFFFF, x=156, y=110, background_color=0x444444)
eco2_text = label.Label(tiny_font, text="eCO2", color=0x000000, x=218, y=8, background_color=0xBBBBBB)
eco2_text.anchor_point = (0.5, 0)
eco2_text.anchored_position = (245, 8)
eco2_label = label.Label(small_font, text="000 ppm", color=0x000000, x=218, y=20, background_color=0xBBBBBB)
eco2_label.anchor_point = (0.5, 0)
eco2_label.anchored_position = (245, 20)
tvoc_text = label.Label(tiny_font, text="TVOC", color=0x000000, x=218, y=8, background_color=0xBBBBBB)
tvoc_text.anchor_point = (0.5, 0)
tvoc_text.anchored_position = (245, 50)
tvoc_label = label.Label(small_font, text="0 ppb", color=0x000000, x=218, y=70, background_color=0xBBBBBB)
tvoc_label.anchor_point = (0.5, 0)
tvoc_label.anchored_position = (245, 62)

# Compose group
group.append(rect1)
group.append(rect2)
group.append(rect3)
group.append(temperature_label)
group.append(humidity_label)
group.append(pressure_label)
group.append(eco2_text)
group.append(eco2_label)
group.append(tvoc_text)
group.append(tvoc_label)
group.append(temperature_tile)
group.append(humidity_tile)
group.append(pressure_tile)

print("Running loop")
remaining_time = 0

while True:
    remaining_time -= 1
    if remaining_time <= 0:
        remaining_time = 5 * 60

        print("========================")
#        print('BME Temperature: {} C'.format(bme680_sensor.temperature))
#        print('BME Gas: {} ohms'.format(bme680_sensor.gas))
#        print('BME Humidity: {}%'.format(bme680_sensor.humidity))
#        print('BME Pressure: {}hPa'.format(bme680_sensor.pressure))
#        print("SGP eCO2 = %d ppm" % (sgp30_sensor.eCO2))
#        print("SGP TVOC = %d ppb" % (sgp30_sensor.TVOC))

#        temperature_label.text = "{:4.1f}°".format(bme680_sensor.temperature)
#        humidity_label.text = "{:4.1f}%".format(bme680_sensor.humidity)
#        pressure_label.text = "{:4.0f} hPa".format(bme680_sensor.pressure)
#        eco2_label.text = "{:4.0f} ppm".format(sgp30_sensor.eCO2)
#        tvoc_label.text = "{:4.0f} ppb".format(sgp30_sensor.TVOC)

        temp_f = dps310.temperature * 1.8 + 32
        temperature_label.text = "{:4.1f}°".format(temp_f)
        humidity_label.text = "{:4.1f}%".format(0.0)
        pressure_label.text = "{:5.0f} hPa".format(dps310.pressure)
 #       eco2_label.text = "{:4.0f} ppm".format(123.4)
 #       tvoc_label.text = "{:4.0f} ppb".format(123.4)
        display.show(group)
        display.refresh()
    time.sleep(1)
