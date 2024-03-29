import MySQLdb

# Configure the database connection
db_config = {
    'host': 'localhost',
    'user': 'admin',  # Replace 'username' with your MySQL username
    'passwd': 'admin',  # Replace 'password' with your MySQL password
    'db': 'fastapi',  # Replace 'dbname' with your MySQL database name
}

# Establish a connection to the database
conn = MySQLdb.connect(**db_config)
cursor = conn.cursor()

# Create the notes table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50),
        description VARCHAR(255)
    )
""")

# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cursor.close()
conn.close()