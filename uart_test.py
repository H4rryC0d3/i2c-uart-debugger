import serial
import time
import logging
from datetime import datetime

LOG_FILE = "uart_debug.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

baud_rates = [9600, 19200, 38400, 57600, 115200]
data_bits = [serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS]
parity_list = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD]
stop_bits = [serial.STOPBITS_ONE, serial.STOPBITS_TWO]

PORT = '/dev/ttyUSB0'

def test_uart():
    logging.info("===== UART TEST START =====")
    logging.info(f"Start Time: {datetime.now()}")
    logging.info("Baud,DataBits,Parity,StopBits,Result,Response")

    for baud in baud_rates:
        for db in data_bits:
            for parity in parity_list:
                for sb in stop_bits:
                    timestamp = datetime.now()
                    try:
                        ser = serial.Serial(
                            port=PORT,
                            baudrate=baud,
                            bytesize=db,
                            parity=parity,
                            stopbits=sb,
                            timeout=0.2
                        )
                        test_msg = b'\n'
                        ser.write(test_msg)
                        time.sleep(0.1)
                        response = ser.read(10)

                        if response == test_msg:
                            result = "PASS"
                        elif response:
                            result = "DATA MISMATCH"
                        else:
                            result = "FAIL"
                        ser.close()
                    except Exception as e:
                        result = "ERROR"
                        response = str(e)

                    log_line = f"{timestamp},{baud},{db},{parity},{sb},{result},{response}"
                    logging.info(log_line)

    logging.info(f"End Time: {datetime.now()}")
    logging.info("===== UART TEST END =====")

if __name__ == "__main__":
    test_uart()
    print(f"[UART] Logs saved in {LOG_FILE}")

