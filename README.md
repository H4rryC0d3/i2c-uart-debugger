# 🔧 I2C-UART Debugger

💡 Supports **I2C + UART Debugging with OLED Display & Web Dashboard**

---

## 📌 Overview

**I2C-UART Debugger** is a Raspberry Pi-based embedded system tool designed to **test, analyze, and debug communication protocols** like I2C and UART.

It helps identify hardware and communication issues by running multiple test cases and displaying results on:

* Terminal
* OLED Display (I2C)
* Web Dashboard (Flask)
* Log Files

---

## 🚀 Features

* ✅ I2C communication testing (multiple test cases)
* ✅ UART communication testing & monitoring
* ✅ OLED display for real-time results
* ✅ Flask-based web dashboard
* ✅ Parallel test execution
* ✅ Log file generation for debugging
* ✅ Modular and scalable design

---

## 🧩 Supported Protocols

### 🔹 I2C (Inter-Integrated Circuit)

* NO ACK Detection
* Bus Stuck Detection
* Clock Test
* Arbitration Check
* Device Scan
* Pull-up Verification

---

### 🔹 UART (Universal Asynchronous Receiver/Transmitter)

* Data Transmission Test
* Data Reception Test
* Loopback Test
* Baud Rate Validation
* Timeout/Error Handling

---

## 🛠️ Hardware Requirements

* Raspberry Pi
* OLED Display (SSD1306 - I2C)
* I2C Device (EEPROM / Sensor)
* UART Device (or loopback connection)
* Jumper Wires

---

## 🔌 Connections

### I2C (OLED + Device)

| OLED Pin | Raspberry Pi Pin |
| -------- | ---------------- |
| VCC      | 3.3V / 5V        |
| GND      | GND              |
| SDA      | GPIO2 (Pin 3)    |
| SCL      | GPIO3 (Pin 5)    |

---

### UART

| UART Pin | Raspberry Pi Pin |
| -------- | ---------------- |
| TX       | RX (GPIO15)      |
| RX       | TX (GPIO14)      |
| GND      | GND              |

👉 For testing: connect **TX ↔ RX (Loopback)**

---

## ⚙️ Software Requirements

* Python 3
* smbus / smbus2
* pyserial
* Flask
* OLED library (SSD1306)

---

## 📂 Project Structure

```
i2c-uart-debugger/
│── main.py
│── i2c_handler.py
│── uart_test.py
│── display.py
│── config.py
│── parallel_runner.py
│── server.py
│── logs/
│    ├── i2c_debug.log
│    ├── uart_debug.log
```

---

## ▶️ How to Run

### 1️⃣ Clone Repository

```
git clone https://github.com/<your-username>/i2c-uart-debugger.git
cd i2c-uart-debugger
```

---

### 2️⃣ Install Dependencies

```
pip3 install smbus2 pyserial flask luma.oled
```

---

### 3️⃣ Run Project

#### ▶ Run Main System

```
python3 main.py
```

#### 🌐 Run Web Dashboard

```
python3 server.py
```

---

## 🌐 Web Dashboard

* Real-time log streaming
* Monitor I2C & UART results in browser
* Parallel execution support
* Lightweight Flask UI

---

## 📊 Sample Output

### Terminal

```
I2C TEST RESULTS
NO ACK          : FAIL
BUS STUCK       : PASS
CLOCK           : PASS
SCAN            : PASS

UART TEST RESULTS
TX TEST         : PASS
RX TEST         : PASS
LOOPBACK        : PASS
BAUD RATE       : PASS
```

---

### OLED Display

```
I2C + UART TEST
RUNNING...
RESULT: PASS
```

---

## 📁 Log Files

* logs/i2c_debug.log → stores I2C test results
* logs/uart_debug.log → stores UART test results

---

## 🎯 Applications

* Embedded System Debugging
* Hardware Testing & Validation
* IoT Device Development
* Communication Protocol Analysis

---

## ⚡ Challenges Faced

* I2C timeout and address conflicts
* OLED display initialization issues
* UART baud rate mismatch
* Serial communication delays

---

## 🔮 Future Improvements

* Add SPI protocol support
* Advanced UI with graphs
* Error alert system
* Remote monitoring

---

## 📜 License

This project is open-source and available under the MIT License.
