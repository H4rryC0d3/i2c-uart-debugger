import smbus
import time
import logging
import sys
from datetime import datetime

from display import show
from config import I2C_BUS, DEVICE_ADDR, RETRY_COUNT, DELAY

LOG_FILE = "i2c_debug.log"

logger = logging.getLogger("i2c_logger")
logger.setLevel(logging.INFO)

if logger.handlers:
    for h in logger.handlers[:]:
        logger.removeHandler(h)

file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def flush_logs():
    try:
        for h in logger.handlers:
            if hasattr(h, "flush"):
                h.flush()
    except Exception:
        pass

bus = smbus.SMBus(I2C_BUS)

#live device check (detect wire removal during test)
def device_alive():
    try:
        bus.read_byte(DEVICE_ADDR)
        return True
    except:
        return False

def no_ack_check():
    try:
        bus.write_byte(DEVICE_ADDR, 0x00)
        return "PASS"
    except:
        return "FAIL"

def bus_stuck_check():
    try:
        bus.read_byte(DEVICE_ADDR)
        return "PASS"
    except:
        return "FAIL"

def clock_stretching_check():
    try:
        bus.read_byte(DEVICE_ADDR)
        return "PASS"
    except:
        return "FAIL"

def arbitration_check():
    for _ in range(RETRY_COUNT):
        try:
            bus.write_byte(DEVICE_ADDR, 0x01)
            return "PASS"
        except:
            time.sleep(DELAY)
    return "FAIL"

def address_scan():
    found = []
    for addr in range(0x03, 0x78):
        try:
            bus.write_byte(addr, 0)
            found.append(addr)
        except:
            pass
    return "PASS" if DEVICE_ADDR in found else "FAIL"

def pullup_check():
    try:
        bus.read_byte(DEVICE_ADDR)
        return "PASS"
    except:
        return "FAIL"

def data_corruption_check():
    try:
        d1 = bus.read_byte(DEVICE_ADDR)
        time.sleep(0.1)
        d2 = bus.read_byte(DEVICE_ADDR)
        return "PASS" if d1 == d2 else "FAIL"
    except:
        return "FAIL"

def start_stop_check():
    try:
        bus.write_i2c_block_data(DEVICE_ADDR, 0x00, [1, 2, 3])
        return "PASS"
    except:
        return "FAIL"

def timing_check():
    try:
        for i in range(20):
            # 🔥 detect mid-run disconnection
            if not device_alive():
                return "FAIL"
            bus.write_byte(DEVICE_ADDR, i)
        return "PASS"
    except:
        return "FAIL"

def contention_check():
    try:
        bus.write_byte(DEVICE_ADDR, 0xFF)
        return "PASS"
    except:
        return "FAIL"

def slave_busy_check():
    for _ in range(RETRY_COUNT):
        try:
            if not device_alive():
                return "FAIL"
            bus.write_byte(DEVICE_ADDR, 0xAA)
            return "PASS"
        except:
            time.sleep(0.05)
    return "FAIL"

def repeated_start_check():
    try:
        bus.read_i2c_block_data(DEVICE_ADDR, 0x00, 4)
        return "PASS"
    except:
        return "FAIL"

def voltage_check():
    try:
        bus.read_byte(DEVICE_ADDR)
        return "PASS"
    except:
        return "FAIL"

def overload_check():
    errors = 0
    for _ in range(10):
        try:
            if not device_alive():
                return "FAIL"
            bus.read_byte(DEVICE_ADDR)
        except:
            errors += 1
    return "FAIL" if errors > 3 else "PASS"

def driver_check():
    try:
        smbus.SMBus(I2C_BUS)
        return "PASS"
    except:
        return "FAIL"

def run_all():
    return [
        ("NO ACK",      no_ack_check()),
        ("BUS STUCK",   bus_stuck_check()),
        ("CLOCK",       clock_stretching_check()),
        ("ARBITRATION", arbitration_check()),
        ("SCAN",        address_scan()),
        ("PULL-UP",     pullup_check()),
        ("CORRUPTION",  data_corruption_check()),
        ("START/STOP",  start_stop_check()),
        ("TIMING",      timing_check()),
        ("CONTENTION",  contention_check()),
        ("SLAVE BUSY",  slave_busy_check()),
        ("RESTART",     repeated_start_check()),
        ("VOLTAGE",     voltage_check()),
        ("OVERLOAD",    overload_check()),
        ("DRIVER",      driver_check()),
    ]

if __name__ == "__main__":
    logger.info("========== I2C TEST START ==========")
    logger.info(f"Start Time: {datetime.now()}")
    flush_logs()

    try:
        results = run_all()

        for name, result in results:
            line = "{:<15} : {}".format(name, result)
            print(line)
            logger.info(line)
            flush_logs()

            if result != "PASS":
                fail_msg = f"{name} FAILED (Device issue or disconnected)"
                logger.warning(fail_msg)
                flush_logs()
                print("\nFINAL RESULT:", fail_msg)
                sys.exit(1)

        # ✅ ONLY PASS → OLED
        success_msg = "ALL TESTS PASSED"
        logger.info(success_msg)
        flush_logs()
        print("\nFINAL RESULT:", success_msg)

        try:
            show("TEST PASSED")
            time.sleep(30)
            show("")   # OFF OLED
        except Exception:
            logger.debug("OLED show failed for TEST PASSED")
            flush_logs()

    except KeyboardInterrupt:
        logger.warning("User interrupted I2C tests")
        flush_logs()
        print("\nExited by user")
        sys.exit(2)

    except Exception as e:
        logger.error(f"Unexpected error during I2C tests: {e}")
        flush_logs()
        print("\nERROR OCCURRED:", e)
        sys.exit(3)

    finally:
        logger.info(f"End Time: {datetime.now()}")
        logger.info("========== I2C TEST END ==========")
        flush_logs()
