import sqlite3

def create_db():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        con = sqlite3.connect(database=r'attendance_system.db')
        cur = con.cursor()

        # Create the 'Teachers' table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Teachers (
            TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
        """)

        # Create the 'students' table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch TEXT,
            course TEXT,
            semester TEXT,
            name TEXT,
            usn TEXT,
            gender TEXT,
            dob TEXT,
            email TEXT UNIQUE,
            phone TEXT
        )
        """)

        # Commit the changes
        con.commit()

        print("Database and tables created successfully.")

    except sqlite3.Error as e:
        print(f"Error while creating database: {e}")

    finally:
        # Ensure the connection is closed
        if con:
            con.close()

# Call the function to create the database and tables
create_db()
