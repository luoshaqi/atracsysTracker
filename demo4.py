import time
from pyper.viper_classes import PolhemusViper

def main():
    # 创建Viper对象
    viper = PolhemusViper()

    try:
        # 连接到Viper设备
        viper.connect()

        # 启用数据传输模式
        # viper.start_streaming()

        # 读取数据
        while True:
            # 读取一条数据
            data = viper.get_single_pno(pno_mode="standard")

            # 打印数据
            print(data)

            # 可以加入其他处理数据的逻辑

            # 延迟一段时间，例如0.1秒
            time.sleep(0.1)

    except KeyboardInterrupt:
        # 如果用户按下Ctrl+C，退出程序
        print("Program terminated by user.")
    except Exception as e:
        print("Error:", e)
    finally:
        # 断开与设备的连接
        # viper.disconnect()
        pass

if __name__ == "__main__":
    main()
