import sqlite3
import math

DB_NAME = "cities.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        latitude REAL,
        longitude REAL
    )
    """)
    conn.commit()
    conn.close()

def get_city_coords(city_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT latitude, longitude FROM cities WHERE name = ?", (city_name,))
    result = cur.fetchone()
    conn.close()
    return result

def add_city(city_name, latitude, longitude):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO cities (name, latitude, longitude) VALUES (?, ?, ?)", (city_name, latitude, longitude))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"City {city_name} already exists in database.")
    conn.close()

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    R = 6371  # Earth's radius in kilometers
    distance = R * c
    return distance

def get_city_coordinates_from_user(city_name):
    while True:
        try:
            lat = float(input(f"Enter latitude for {city_name} (in decimal degrees, e.g. 50.45): "))
            lon = float(input(f"Enter longitude for {city_name} (in decimal degrees, e.g. 30.52): "))
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                print("Coordinates out of valid range. Try again.")
                continue
            return lat, lon
        except ValueError:
            print("Invalid input. Please enter valid decimal numbers.")

def main():
    create_table()

    city1 = input("Enter first city name: ").strip()
    city2 = input("Enter second city name: ").strip()

    coords1 = get_city_coords(city1)
    if coords1 is None:
        print(f"Coordinates for {city1} not found.")
        lat, lon = get_city_coordinates_from_user(city1)
        add_city(city1, lat, lon)
        coords1 = (lat, lon)

    coords2 = get_city_coords(city2)
    if coords2 is None:
        print(f"Coordinates for {city2} not found.")
        lat, lon = get_city_coordinates_from_user(city2)
        add_city(city2, lat, lon)
        coords2 = (lat, lon)

    distance = haversine(coords1[0], coords1[1], coords2[0], coords2[1])
    print(f"Distance between {city1} and {city2} is {distance:.2f} kilometers.")

if __name__ == "__main__":
    main()
