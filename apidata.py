import requests
import mysql.connector
from mysql.connector import Error

# -------------------------
# DATABASE CONNECTION
# -------------------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",              # change if your MySQL username differs
            password="1234",  # change to your MySQL password
            database="sports"
        )
        if conn.is_connected():
            print("✅ Connected to MySQL Database")
        return conn
    except Error as e:
        print("❌ Error connecting to MySQL:", e)
        return None


# -------------------------
# CREATE TABLES
# -------------------------
def create_tables(conn):
    cursor = conn.cursor()

    # Drop existing tables (clean reset)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS Competitor_Rankings;")
    cursor.execute("DROP TABLE IF EXISTS Competitors;")
    cursor.execute("DROP TABLE IF EXISTS Venues;")
    cursor.execute("DROP TABLE IF EXISTS Complexes;")
    cursor.execute("DROP TABLE IF EXISTS Competitions;")
    cursor.execute("DROP TABLE IF EXISTS Categories;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # Create fresh tables
    cursor.execute("""
    CREATE TABLE Categories (
        category_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    cursor.execute("""
    CREATE TABLE Competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        category_id VARCHAR(50),
        gender VARCHAR(20),
        type VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
            ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    cursor.execute("""
    CREATE TABLE Complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        city VARCHAR(100),
        country VARCHAR(100)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    cursor.execute("""
    CREATE TABLE Venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        capacity INT,
        surface VARCHAR(50),
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
            ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    cursor.execute("""
    CREATE TABLE Competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        nationality VARCHAR(100)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    # ✅ Foreign key types and lengths match exactly with Competitors table
    cursor.execute("""
    CREATE TABLE Competitor_Rankings (
        rank_id INT AUTO_INCREMENT PRIMARY KEY,
        competitor_id VARCHAR(50),
        rank_position INT,
        points INT,
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
            ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    conn.commit()
    cursor.close()
    print("✅ Tables created successfully")


# -------------------------
# MOCK DATA FETCH FUNCTIONS
# (Replace later with real Sportradar API calls)
# -------------------------
def get_competitions_data():
    return {
        "categories": [
            {"id": "cat1", "name": "ATP"},
            {"id": "cat2", "name": "WTA"}
        ],
        "competitions": [
            {"id": "comp1", "name": "Australian Open", "category_id": "cat1", "gender": "male", "type": "grand_slam"},
            {"id": "comp2", "name": "US Open", "category_id": "cat2", "gender": "female", "type": "grand_slam"}
        ]
    }

def get_complexes_data():
    return {
        "complexes": [
            {"id": "complex1", "name": "Melbourne Park", "city": "Melbourne", "country": "Australia"},
            {"id": "complex2", "name": "USTA Billie Jean King National Tennis Center", "city": "New York", "country": "USA"}
        ],
        "venues": [
            {"id": "venue1", "name": "Rod Laver Arena", "capacity": 15000, "surface": "hard", "complex_id": "complex1"},
            {"id": "venue2", "name": "Arthur Ashe Stadium", "capacity": 23000, "surface": "hard", "complex_id": "complex2"}
        ]
    }

def get_doubles_rankings_data():
    return {
        "competitors": [
            {"id": "p1", "name": "John Peers", "nationality": "Australia"},
            {"id": "p2", "name": "Joe Salisbury", "nationality": "UK"}
        ],
        "rankings": [
            {"competitor_id": "p1", "rank": 1, "points": 8000},
            {"competitor_id": "p2", "rank": 2, "points": 7600}
        ]
    }


# -------------------------
# DATA INSERTION FUNCTIONS
# -------------------------
def insert_competitions(conn, data):
    cursor = conn.cursor()
    for cat in data["categories"]:
        cursor.execute("""
            INSERT IGNORE INTO Categories (category_id, name)
            VALUES (%s, %s)
        """, (cat["id"], cat["name"]))

    for comp in data["competitions"]:
        cursor.execute("""
            INSERT IGNORE INTO Competitions (competition_id, name, category_id, gender, type)
            VALUES (%s, %s, %s, %s, %s)
        """, (comp["id"], comp["name"], comp["category_id"], comp["gender"], comp["type"]))

    conn.commit()
    cursor.close()
    print("✅ Competition data inserted")


def insert_complexes(conn, data):
    cursor = conn.cursor()
    for complex_ in data["complexes"]:
        cursor.execute("""
            INSERT IGNORE INTO Complexes (complex_id, name, city, country)
            VALUES (%s, %s, %s, %s)
        """, (complex_["id"], complex_["name"], complex_["city"], complex_["country"]))

    for venue in data["venues"]:
        cursor.execute("""
            INSERT IGNORE INTO Venues (venue_id, name, capacity, surface, complex_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (venue["id"], venue["name"], venue["capacity"], venue["surface"], venue["complex_id"]))

    conn.commit()
    cursor.close()
    print("✅ Complexes & Venues data inserted")


def insert_rankings(conn, data):
    cursor = conn.cursor()
    for comp in data["competitors"]:
        cursor.execute("""
            INSERT IGNORE INTO Competitors (competitor_id, name, nationality)
            VALUES (%s, %s, %s)
        """, (comp["id"], comp["name"], comp["nationality"]))

    for rank in data["rankings"]:
        cursor.execute("""
            INSERT INTO Competitor_Rankings (competitor_id, rank_position, points)
            VALUES (%s, %s, %s)
        """, (rank["competitor_id"], rank["rank"], rank["points"]))

    conn.commit()
    cursor.close()
    print("✅ Competitor & Ranking data inserted")


# -------------------------
# MAIN FUNCTION
# -------------------------
def main():
    conn = connect_db()
    if conn:
        create_tables(conn)

        competitions_data = get_competitions_data()
        insert_competitions(conn, competitions_data)

        complexes_data = get_complexes_data()
        insert_complexes(conn, complexes_data)

        rankings_data = get_doubles_rankings_data()
        insert_rankings(conn, rankings_data)

        conn.close()
        print("🏁 All data successfully loaded into MySQL")


# -------------------------
# RUN SCRIPT
# -------------------------
if __name__ == "__main__":
    main()
