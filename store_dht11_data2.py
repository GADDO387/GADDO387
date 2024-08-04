import serial
import time
import mariadb

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Connect to MariaDB database
db = mariadb.connect(
    host="172.20.10.4",
    user="Gaddo",  # Replace with your MariaDB username
    password="12345",  # Replace with your MariaDB password
    database="sensor_data"  # Updated database name
)

cursor = db.cursor()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        
        # Parse the line for humidity, temperature, and luxvalue
        try:
            if "Average Humidity:" in line:
                humidity = float(line.split(": ")[1].replace(" RH", ""))
                line = ser.readline().decode('utf-8').rstrip()
                avgTempC = float(line.split(": ")[1].replace("°C", ""))
                line = ser.readline().decode('utf-8').rstrip()
                avgTempF = float(line.split(": ")[1].replace("°F", ""))
                line = ser.readline().decode('utf-8').rstrip()
                luxvalue = float(line.split(": ")[1])  # Assuming the line contains lux value

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
