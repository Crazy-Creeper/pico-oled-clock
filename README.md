# pico-oled-clock
A Micropython script for NTP time sync and display on OLED. 

CN：
这段代码是用 MicroPython 在树莓派 Raspberry Pi Pico w 上实现连接 Wi-Fi、获取时间并显示在 SSD1306 OLED 显示屏上的代码。

代码的具体功能如下：

连接 Wi-Fi 网络
获取当前时间，并将其显示在 OLED 屏幕上
每隔一天更新时间，以防止时间漂移
代码首先会连接 Wi-Fi 网络，连接成功后，代码将显示 “Connect Success” 消息，并在 OLED 屏幕上显示当前日期和时间。在每隔一秒钟更新 OLED 屏幕上的时间，并检查是否应该更新时间。如果当前时间是午夜（即小时、分钟和秒数均为0），则将调用 set_time() 函数更新时间。

该代码使用了 socket 和 struct 库以获取 NTP 服务器的时间，并使用 machine 库访问 RTC（实时时钟）以设置和获取当前时间。此外，它还使用了 network 库以连接 Wi-Fi 网络。 OLED 屏幕的控制使用了 SSD1306_I2C 类。

值得注意的是，该代码仅用于演示 MicroPython 和树莓派 Pico 上使用 OLED 屏幕。如果您要在生产环境中使用该代码，请务必对其进行适当的测试和修改，以确保其适用于您的应用程序和硬件环境。


EN：
This code is written in MicroPython and runs on a Raspberry Pi Pico to connect to Wi-Fi, get the time, and display it on an SSD1306 OLED display.

The specific functions of the code are as follows:

Connect to a Wi-Fi network
Get the current time and display it on an OLED screen
Update the time every day to prevent time drift
The code first connects to a Wi-Fi network. Once the connection is successful, the code will display a "Connect Success" message and show the current date and time on the OLED screen. The OLED screen updates every second to display the current time and checks if the time needs to be updated. If the current time is midnight (i.e. hours, minutes, and seconds are all 0), the set_time() function is called to update the time.

The code uses the socket and struct libraries to get the time from an NTP server and uses the machine library to access the RTC (real-time clock) to set and get the current time. Additionally, it uses the network library to connect to a Wi-Fi network. Control of the OLED screen is done using the SSD1306_I2C class.

It is worth noting that this code is for demonstration purposes only and is intended to show how to use an OLED screen with MicroPython on a Raspberry Pi Pico. If you plan to use this code in a production environment, be sure to test and modify it appropriately to ensure that it is suitable for your application and hardware environment.
