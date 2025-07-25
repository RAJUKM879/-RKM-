import mysql.connector
import pandas as pd

# Step 1: Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""  # Add password if set
)
cursor = conn.cursor()

# Step 2: Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
print("✅ Database 'student_db' ensured.")

# Step 3: Connect to the database
conn.database = "student_db"

# Step 4: Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    grade VARCHAR(10)
)
""")
print("✅ Table 'students' ensured.")

# Step 5: Insert manual data
sample_data = [("Alice", 20, "A"), ("Bob", 22, "B"), ("Charlie", 19, "A")]
cursor.executemany("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", sample_data)
conn.commit()
print("✅ Sample data inserted.")

# Step 6: Insert data from CSV
try:
    df = pd.read_csv("students.csv")  # Place CSV file in same folder
    df.columns = df.columns.str.strip().str.lower()
    for _, row in df.iterrows():
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
                       (row["name"], int(row["age"]), row["grade"]))
    conn.commit()
    print("✅ Data from CSV inserted.")
except FileNotFoundError:
    print("⚠️ CSV file not found. Skipping...")
except Exception as e:
    print("❌ Error:", e)

# Step 7: Fetch and display data
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
print("🎉 All done!")
