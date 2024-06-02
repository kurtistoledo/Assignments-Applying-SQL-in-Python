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

def get_members_in_age_range(conn, start_age, end_age):
    """Retrieve the details of members whose ages fall between start_age and end_age."""
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT id, name, age 
        FROM Members 
        WHERE age BETWEEN ? AND ?;
        """, (start_age, end_age))
        
        rows = cur.fetchall()
        
        if rows:
            print(f"Members between ages {start_age} and {end_age}:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
        else:
            print(f"No members found between ages {start_age} and {end_age}.")
    except Error as e:
        print(f"Error retrieving members in age range: {e}")

def main():
    database = "gym_management.db"

    # Create a database connection
    conn = create_connection(database)

    if conn is not None:
        # Example usage
        get_members_in_age_range(conn, 25, 30)
        
        # Close the connection
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()
