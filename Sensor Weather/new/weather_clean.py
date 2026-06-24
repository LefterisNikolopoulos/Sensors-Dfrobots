#!/usr/bin/env python3
# weather_clean.py
import serial
import json
import time
import sys

def read_weather_data():
    """Διαβάζει δεδομένα από τον αισθητήρα καιρού"""
    try:
        # Σύνδεση με τη σειριακή θύρα
        ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=10
        )
        
        # Διάβασε γραμμές μέχρι να βρείς δεδομένα καιρού
        for _ in range(20):
            try:
                line_bytes = ser.readline()
                if line_bytes:
                    line = line_bytes.decode('utf-8', errors='ignore').strip()
                    
                    # Αγνόησε κενές γραμμές και AT commands
                    if not line or line.startswith('AT') or line.startswith('TIME') or line.startswith('BH'):
                        continue
                    
                    # Ελέγξε αν είναι δεδομένα καιρού
                    if line.startswith('c') and len(line) >= 33:
                        # Parse τα δεδομένα
                        wind_dir = int(line[1:4])
                        wind_speed_mph = int(line[5:8])
                        wind_gust_mph = int(line[9:12])
                        temp_f = int(line[13:16])
                        rain_1h = int(line[17:20])
                        rain_24h = int(line[21:24])
                        humidity = int(line[25:27])
                        pressure_mb_x10 = int(line[28:33])
                        
                        # Μετατροπές μονάδων
                        wind_speed_ms = wind_speed_mph * 0.44704
                        wind_gust_ms = wind_gust_mph * 0.44704
                        temp_c = (temp_f - 32) * 5 / 9
                        rain_1h_mm = rain_1h * 0.254
                        rain_24h_mm = rain_24h * 0.254
                        pressure_hpa = pressure_mb_x10 / 10.0
                        
                        # Κλείσε τη σύνδεση
                        ser.close()
                        
                        return {
                            "sensor_id": "sensor2",
                            "windDirection": wind_dir,
                            "windSpeed": round(wind_speed_ms, 2),
                            "windGust": round(wind_gust_ms, 2),
                            "temperature": round(temp_c, 2),
                            "rainfall1h": round(rain_1h_mm, 2),
                            "rainfall24h": round(rain_24h_mm, 2),
                            "humidity": humidity,
                            "pressure": round(pressure_hpa, 1)
                        }
            
            except (UnicodeDecodeError, ValueError) as e:
                # Συνέχισε αν υπάρχει σφάλμα στην τρέχουσα γραμμή
                continue
        
        # Αν δεν βρέθηκαν δεδομένα
        ser.close()
        return {"error": "No weather data found"}
        
    except serial.SerialException as e:
        return {"error": f"Serial port error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def main():
    """Κύρια συνάρτηση - επιστρέφει μόνο JSON"""
    data = read_weather_data()
    print(json.dumps(data))

if __name__ == "__main__":
    main()
