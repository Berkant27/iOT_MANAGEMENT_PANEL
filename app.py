from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Veritabanı başlatma
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 type TEXT NOT NULL,
                 status TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS device_data (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 device_id INTEGER,
                 data_type TEXT NOT NULL,
                 value REAL NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (device_id) REFERENCES devices(id))''')
    conn.commit()
    conn.close()

init_db()

# MQTT ayarları
def setup_mqtt():
    def on_connect(client, userdata, flags, rc):
        print("MQTT’ye bağlandı")
        client.subscribe("iot/devices/#")

    def on_message(client, userdata, msg):
        device_id = msg.topic.split('/')[-1]
        try:
            value = float(msg.payload.decode())
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO device_data (device_id, data_type, value) VALUES (?, ?, ?)",
                      (device_id, "temperature", value))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"MQTT veri hatası: {e}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("test.mosquitto.org", 1883, 60)
        client.loop_start()
    except Exception as e:
        print(f"MQTT bağlantı hatası: {e}")
    return client

mqtt_client = setup_mqtt()

@app.route('/')
def index():
    return render_template('ındex.html')

@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        status = request.form['status']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO devices (name, type, status) VALUES (?, ?, ?)", (name, type, status))
        conn.commit()
        conn.close()
        return redirect('/devices')
    return render_template('add_device.html')

@app.route('/devices')
def devices():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    devices = c.fetchall()
    conn.close()
    return render_template('device_list.html', devices=devices)

@app.route('/toggle/<int:device_id>/<status>')
def toggle(device_id, status):
    mqtt_client.publish(f"iot/devices/{device_id}/control", status)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE devices SET status=? WHERE id=?", (status, device_id))
    conn.commit()
    conn.close()
    return redirect('/devices')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT device_id, data_type, value, timestamp FROM device_data WHERE data_type='temperature' ORDER BY timestamp DESC LIMIT 10")
    data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)