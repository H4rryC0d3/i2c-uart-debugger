import subprocess
import time
import os
import signal

def run_parallel():
    # Start I2C (main.py) and UART (uart_test.py) in parallel.
    # Each script writes to its own log file; no shared logging.
    p1 = subprocess.Popen(["python3", "main.py"])
    time.sleep(1)  # small stagger so I2C starts first
    p2 = subprocess.Popen(["python3", "uart_test.py"])

    try:
        while True:
            p1_done = (p1.poll() is not None)
            p2_done = (p2.poll() is not None)

            if p1_done and p2_done:
                break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping all tests (KeyboardInterrupt)...")
        for p in (p1, p2):
            try:
                p.send_signal(signal.SIGTERM)
            except Exception:
                pass
        raise

    print("=== ALL TESTS COMPLETED ===")
    # return exit codes for caller if needed
    return (p1.returncode, p2.returncode)

if __name__ == "__main__":
    run_parallel()

