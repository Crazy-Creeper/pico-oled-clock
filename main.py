import network
import socket
import time
import utime
import struct
import machine
from machine import Pin
from ssd1306 import SSD1306_I2C   # 提供控制SSD1306显示屏的类

NTP_DELTA = 2208988800
# ntp host
host = "cn.ntp.org.cn"
#初始化led
led = Pin("LED", Pin.OUT)
led.on()
utime.sleep(1)
led.off()

#init RTC
rtc = machine.RTC()
print(rtc.datetime())

# init Pin
sda = machine.Pin(0)  # SDA引脚
scl = machine.Pin(1)  # SCL引脚
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)  # 创建I2C对象

#使用SSD1306_I2C类创建一个128x32像素的OLED显示屏对象：
oled = SSD1306_I2C(128, 32, i2c)


oled.fill(0)
oled.text("Connecting Wi-Fi", 0, 10)
oled.show()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wifi SSID Password
wlan.connect('creeper', '12222222')

counter = 0
while not wlan.isconnected() and wlan.status() != 3:
    print(wlan.status())
    time.sleep(1)
    counter += 1
    if counter > 30:
        oled.fill(0)
        oled.text("WIFI ERROR", 0, 10)
        oled.show()
        time.sleep(3)
        macmachine.reset()
     
led.on()
oled.fill(0)
oled.text("Connect Success", 0, 10)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()


#ntp同步时间
def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except OSError as e:
        raise RuntimeError("Failed to connect to NTP server: {}".format(e))
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA + 8 * 3600    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
set_time()

# 判断星期几
def switch_case(case):
    return {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Crazy Thursday!',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }.get(case, 'D-Day')

# 展示到oled
while True:
    # 获取当前时间并格式化为字符串
    (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
    time_str1 = "{:04d}-{:02d}-{:02d} W:{:01d}".format(year, month, day, weekday+1)
    time_str2 = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    

    
    # 在 OLED 显示屏上显示时间
    oled.fill(0)
    
    oled.text(time_str1, 0, 0)
    oled.text(switch_case(weekday), 0, 10)
    oled.text(time_str2, 0,20)
    oled.show()
    utime.sleep(1) #等待一秒钟    
    if hours == 0 and minutes == 0 and seconds == 0: # 每隔一天执行一次 set_time()
        set_time()
    



