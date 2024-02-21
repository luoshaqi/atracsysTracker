import serial

# 开启串行通信
ser = serial.Serial(
    port='/dev/ttyUSB0',  # 设备的端口
    baudrate=9600,        # 波特率，这个需要根据你的设备文档来设置
)

# 开始读取数据
while True:
    if ser.in_waiting:
        data = ser.readline().decode('utf-8').strip()  # 读取一行数据
        print(data)  # 打印数据，或者处理数据