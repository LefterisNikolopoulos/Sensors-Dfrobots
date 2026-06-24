import serial
from datetime import datetime

# ➤ Open the serial port to communicate with the sensor
ser = serial.Serial('/dev/serial0', 9600, timeout=5)

# ➤ Function to parse a single line from the sensor and return a dictionary of values
def parse_line(line):
    try:
        # If the line doesn't start with 'c', it's not valid data
        if not line.startswith('c'):
            return None

        # ➤ Parse and convert sensor data values
        windDirection = int(line[1:4])  # Wind direction in degrees
        windSpeed = int(line[5:8]) * 0.44704  # Wind speed converted from mph to m/s
        windGust = int(line[9:12]) * 0.44704  # Wind gust speed converted from mph to m/s
        tempF = int(line[13:16])  # Temperature in Fahrenheit
        temperature = (tempF - 32) * 5 / 9  # Convert temperature to Celsius
        rainfall1h = int(line[17:20]) * 0.254  # Rainfall last 1 hour in mm (from inches)
        rainfall24h = int(line[21:24]) * 0.254  # Rainfall last 24 hours in mm (from inches)
        humidity = int(line[25:27])  # Humidity in percentage
        pressure = int(line[28:33]) / 10  # Atmospheric pressure in hPa

        # Return parsed values as a dictionary
        return {
            "windDirection": windDirection,
            "windSpeed": windSpeed,
            "windGust": windGust,
            "temperature": temperature,
            "rainfall1h": rainfall1h,
            "rainfall24h": rainfall24h,
            "humidity": humidity,
            "pressure": pressure
        }
    except Exception as e:
        # Print error if parsing fails and return None
        print(f"Error parsing line: {e}")
        return None

print("Started data logging...\n")

while True:
    try:
        # Read a line from the serial port, decode to string and strip whitespace
        line = ser.readline().decode('utf-8').strip()
        data = parse_line(line)
        if data is None:
            continue

        # Define if it is raining based on rainfall last 1 hour threshold
        rain = 1 if data["rainfall1h"] > 0.2 else 0

        # Current timestamp formatted as string
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print all sensor values with units
        print(f"[{timestamp}]")
        print(f"windDirection: {data['windDirection']}°")
        print(f"windSpeed: {data['windSpeed']:.2f} m/s")
        print(f"windGust: {data['windGust']:.2f} m/s")
        print(f"temperature: {data['temperature']:.2f} °C")
        print(f"rainfall1h: {data['rainfall1h']:.2f} mm")
        print(f"rainfall24h: {data['rainfall24h']:.2f} mm")
        print(f"humidity: {data['humidity']} %")
        print(f"pressure: {data['pressure']} hPa")
        print()

    except KeyboardInterrupt:
        # Exit cleanly if user presses Ctrl+C
        print("\nTerminated by user.")
        break
