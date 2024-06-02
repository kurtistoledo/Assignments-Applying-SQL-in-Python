

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database {db_file}")
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create the Members and WorkoutSessions tables."""
    try:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS WorkoutSessions (
            session_id INTEGER PRIMARY KEY,
            member_id INTEGER,
            session_date TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            calories_burned INTEGER NOT NULL,
            FOREIGN KEY (member_id) REFERENCES Members (id)
        );
        """)
        conn.commit()
        print("Tables created successfully.")
    except Error as e:
        print(e)

def add_member(conn, id, name, age):
    """Add a new member to the Members table."""
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Members (id, name, age) VALUES (?, ?, ?)", (id, name, age))
        conn.commit()
        print(f"Member {name} added successfully.")
    except Error as e:
        print(f"Error adding member: {e}")

def add_workout_session(conn, member_id, session_date, duration_minutes, calories_burned):
    """Add a new workout session to the WorkoutSessions table."""
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO WorkoutSessions (member_id, session_date, duration_minutes, calories_burned) VALUES (?, ?, ?, ?)",
                    (member_id, session_date, duration_minutes, calories_burned))
        conn.commit()
        print("Workout session added successfully.")
    except Error as e:
        print(f"Error adding workout session: {e}")

def update_member_age(conn, member_id, new_age):
    """Update the age of a member."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Members WHERE id = ?", (member_id,))
        member = cur.fetchone()
        if member:
            cur.execute("UPDATE Members SET age = ? WHERE id = ?", (new_age, member_id))
            conn.commit()
            print(f"Member {member_id}'s age updated to {new_age}.")
        else:
            print(f"Member with ID {member_id} not found.")
    except Error as e:
        print(f"Error updating member age: {e}")

def delete_workout_session(conn, session_id):
    """Delete a workout session based on its session ID."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM WorkoutSessions WHERE session_id = ?", (session_id,))
        session = cur.fetchone()
        if session:
            cur.execute("DELETE FROM WorkoutSessions WHERE session_id = ?", (session_id,))
            conn.commit()
            print(f"Workout session {session_id} deleted successfully.")
        else:
            print(f"Workout session with ID {session_id} not found.")
    except Error as e:
        print(f"Error deleting workout session: {e}")

def main():
    database = "gym_management.db"

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        create_tables(conn)
    else:
        print("Error! Cannot create the database connection.")

    # Example usage
    add_member(conn, 1, "Jane Doe", 30)
    add_member(conn, 2, "John Smith", 28)
    
    add_workout_session(conn, 1, "2024-05-31", 60, 500)
    add_workout_session(conn, 2, "2024-05-31", 45, 300)

    update_member_age(conn, 1, 31)
    
    delete_workout_session(conn, 1)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
