import smbus
import time
from config import I2C_BUS, DEVICE_ADDR, RETRY_COUNT, DELAY

bus = smbus.SMBus(I2C_BUS)

def safe_write(value):
    for i in range(RETRY_COUNT):
        try:
            bus.write_byte(DEVICE_ADDR, value)
            return "Write Success"
        except OSError as e:
            time.sleep(DELAY)
    return "Write Failed (No ACK / Bus Issue)"

def safe_read():
    for i in range(RETRY_COUNT):
        try:
            data = bus.read_byte(DEVICE_ADDR)
            return f"Read Success: {data}"
        except OSError:
            time.sleep(DELAY)
    return "Read Failed"

def check_device():
    try:
        bus.write_byte(DEVICE_ADDR, 0)
        return "Device Found (ACK)"
    except:
        return "Device NOT Found"

def scan_bus():
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.write_byte(addr, 0)
            found.append(hex(addr))
        except:
            pass
    return found if found else ["No devices"]

def detect_data_corruption():
    try:
        d1 = bus.read_byte(DEVICE_ADDR)
        time.sleep(0.1)
        d2 = bus.read_byte(DEVICE_ADDR)
        if d1 != d2:
            return "Data Corruption Detected"
        return "Data OK"
    except:
        return "Read Error"

def check_bus():
    try:
        bus.read_byte(DEVICE_ADDR)
        return "Bus OK"
    except:
        return "Bus Stuck / Issue"