import serial
import time
from ps2_config import *


# Khởi tạo đối tượng serial với các thông số cần thiết
ser = serial.Serial(
    port='COM3',  # Thay đổi thành cổng UART thực tế bạn đang sử dụng
    baudrate=115200,         # Tốc độ baud
    timeout=1              # Timeout cho việc đọc dữ liệu
)



# Hàm gửi dữ liệu qua UART
def send_uart_data(btn):
    for _ in range(10):
        # Chuyển đổi GP_BTN thành chuỗi bytes để gửi qua UART
        for i in btn:
            data = i.to_bytes(1, byteorder='little')
            ser.write(data)
            
        # Thời gian chờ cho việc xử lý trên bên nhận, tùy thuộc vào ứng dụng của bạn
        time.sleep(0.001)  

GP_BTN = [0xFF, 0xFF, 0x7F, 0x7F, 0x7F, 0x7F, GP_MODE_DIGITAL , 0x0D]

def forword():
    GP_BTN[0]  &= ~GP_MASK_UP    # Xoá bit tương ứng với nút UP
    send_uart_data(GP_BTN)
    GP_BTN[0] |= GP_MASK_UP

def backword():
    GP_BTN[0]  &= ~GP_MASK_DOWN    # Xoá bit tương ứng với nút UP
    send_uart_data(GP_BTN)
    GP_BTN[0] |= GP_MASK_DOWN

def turnLeft():
    GP_BTN[0]  &= ~GP_MASK_LEFT    # Xoá bit tương ứng với nút UP
    send_uart_data(GP_BTN)
    GP_BTN[0] |= GP_MASK_LEFT

def turnRight():
    GP_BTN[0]  &= ~GP_MASK_RIGHT    # Xoá bit tương ứng với nút UP
    send_uart_data(GP_BTN)
    GP_BTN[0] |= GP_MASK_RIGHT
    
def stop():
    send_uart_data(GP_BTN)


def delay(_time):
    time.sleep(_time/1000)

forword();
delay(1000);
backword();
delay(1000);
stop()

