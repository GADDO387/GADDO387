import serial
import time
import mariadb

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Connect to MariaDB database
db = mariadb.connect(
    host="localhost",
    user="yourusername",  # Replace with your MariaDB username
    password="yourpassword",  # Replace with your MariaDB password
    database="SensorData"
)

cursor = db.cursor()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        
        # Parse the line for humidity and temperature
        try:
            if "Average Humidity:" in line:
                humidity = float(line.split(": ")[1].replace(" RH", ""))
                line = ser.readline().decode('utf-8').rstrip()
                avgTempC = float(line.split(": ")[1].replace("°C", ""))
                line = ser.readline().decode('utf-8').rstrip()
                avgTempF = float(line.split(": ")[1].replace("°F", ""))
                
                # Insert data into the MariaDB database
                sql = "INSERT INTO DHT11Readings (humidity, temperature) VALUES (?, ?)"
                val = (humidity, avgTempC)
                cursor.execute(sql, val)
                db.commit()

                print(f"Inserted into DB: Humidity={humidity}, Temperature={avgTempC}°C, {avgTempF}°F")
        except Exception as e:
            print(f"Error: {e}")

ser.close()
db.close()
