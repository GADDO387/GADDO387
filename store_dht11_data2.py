import serial
import time
import MySQLdb

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Connect to MariaDB database
db = MySQLdb.connect(
    host="172.20.10.4",
    user="Gaddo",  # Replace with your MariaDB username
    password="12345",  # Replace with your MariaDB password
    database="sensor_data"  # Database name
)

cursor = db.cursor()

while True:
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').rstrip()
            if "Humidity:" in line:
                humidity = float(line.split(": ")[1])

                line = ser.readline().decode('utf-8').rstrip()
                avgTempC = float(line.split(": ")[1])

                line = ser.readline().decode('utf-8').rstrip()
                avgTempF = float(line.split(": ")[1])

                line = ser.readline().decode('utf-8').rstrip()
                luxvalue = float(line.split(": ")[1])

                # Insert data into the MariaDB database
                sql = "INSERT INTO DHT11 (humidity, temperature, luxvalue) VALUES (?, ?, ?)"
                val = (humidity, avgTempC, luxvalue)
                cursor.execute(sql, val)
                db.commit()

                print(f"Inserted into DB: Humidity={humidity}, Temperature={avgTempC}°C, {avgTempF}°F, LuxValue={luxvalue}")

        except Exception as e:
            print(f"Error: {e}")

ser.close()
db.close()

