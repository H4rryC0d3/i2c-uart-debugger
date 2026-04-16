from flask import Flask, Response, jsonify
import subprocess
import time
import threading
import os

app = Flask(__name__)

I2C_LOG  = "i2c_debug.log"
UART_LOG = "uart_debug.log"
PARALLEL_RUNNER = "parallel_runner.py"

def stream_file(path):
    def generate():
        while not os.path.exists(path):
            time.sleep(0.2)
        with open(path, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    yield f"data: {line.rstrip()}\n\n"
                else:
                    time.sleep(0.2)
    return generate

@app.route("/")
def home():
    return """
    <h2>I2C + UART Test Dashboard</h2>
    <button onclick="runTests()">Run Tests</button>
    <button onclick="clearLogs()">Clear Display</button>

    <!-- FIX: working refresh-interval slider -->
    <div style="margin:10px 0; display:flex; align-items:center; gap:10px;">
      <label for="refreshSlider">Log refresh speed:</label>
      <input type="range" id="refreshSlider" min="200" max="5000" step="200" value="200"
             oninput="updateRefresh(this.value)">
      <span id="refreshLabel">200ms</span>
    </div>

    <div style="display:flex; gap:20px;">
      <div style="flex:1;">
        <h3>I2C Logs</h3>
        <pre id="i2c_output" style="height:400px;overflow:auto;background:#111;color:#0f0;padding:10px;"></pre>
      </div>
      <div style="flex:1;">
        <h3>UART Logs</h3>
        <pre id="uart_output" style="height:400px;overflow:auto;background:#111;color:#0f0;padding:10px;"></pre>
      </div>
    </div>

    <script>
    // SSE sources
    const i2cSource  = new EventSource("/stream/i2c_debug.log");
    const uartSource = new EventSource("/stream/uart_debug.log");

    i2cSource.onmessage = function(e) {
        const el = document.getElementById("i2c_output");
        el.innerText += e.data + "\\n";
        el.scrollTop = el.scrollHeight;
    };

    uartSource.onmessage = function(e) {
        const el = document.getElementById("uart_output");
        el.innerText += e.data + "\\n";
        el.scrollTop = el.scrollHeight;
    };

    function runTests() {
        fetch('/run-tests').then(r => r.text()).then(t => console.log(t));
    }

    function clearLogs() {
        document.getElementById("i2c_output").innerText  = "";
        document.getElementById("uart_output").innerText = "";
    }

    // FIX: slider controls how often /status is polled for the terminal title update
    let pollInterval = 200;
    let pollTimer = null;

    function updateRefresh(val) {
        pollInterval = parseInt(val);
        document.getElementById("refreshLabel").innerText = val + "ms";
        restartPoll();
    }

    function restartPoll() {
        if (pollTimer) clearInterval(pollTimer);
        pollTimer = setInterval(pollStatus, pollInterval);
    }

    function pollStatus() {
        fetch('/status').then(r => r.json()).then(data => {
            const i2cLast  = data.i2c_last  && data.i2c_last.length  ? data.i2c_last[0]  : "";
            const uartLast = data.uart_last && data.uart_last.length ? data.uart_last[0] : "";
            document.title = "I2C: " + i2cLast.slice(-40);
        });
    }

    restartPoll();
    </script>
    """

@app.route("/run-tests")
def run_tests():
    def start_runner():
        subprocess.Popen(["python3", PARALLEL_RUNNER])
    t = threading.Thread(target=start_runner, daemon=True)
    t.start()
    return "Tests started"

@app.route("/stream/<logfile>")
def stream(logfile):
    if logfile not in (I2C_LOG, UART_LOG):
        return "Invalid log", 404
    return Response(stream_file(logfile)(), mimetype="text/event-stream")

@app.route("/status")
def status():
    def tail(path, n=1):
        if not os.path.exists(path):
            return []
        with open(path, "rb") as f:
            try:
                f.seek(-1024, 2)
            except OSError:
                f.seek(0)
            data = f.read().decode(errors="ignore").splitlines()
            return data[-n:] if data else []
    return jsonify({
        "i2c_last":  tail(I2C_LOG,  1),
        "uart_last": tail(UART_LOG, 1),
    })

if __name__ == "__main__":
    print("Starting server on port 8000...")
    app.run(host="0.0.0.0", port=8000, threaded=True)
