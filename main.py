import sqlite3
from pandas import DataFrame

# Create a sample database with students' information
conn = sqlite3.connect('student_results.db')
cursor = conn.cursor()

# Create tables for exam scores, subjects, and students
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject TEXT,
        score REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        roll_number TEXT,
        email TEXT
    )
''')

# Insert sample data into tables
for i in range(1, 11):
    cursor.execute("INSERT INTO exams (student_id, subject, score) VALUES (?, 'Math', ?)", (i, i*10))

for j in range(1, 5):
    cursor.execute("INSERT INTO subjects (name) VALUES (?)", ('Science',))

for k in range(1, 11):
    cursor.execute("INSERT INTO students (id, name, roll_number, email) VALUES (?, ?, ?, ?)", (k, f'Student {k}', f'RS{100+k}', f'student{k}@example.com'))

conn.commit()

# Query the database to get student results
cursor.execute('''
    SELECT s.name, e.subject, AVG(e.score) as average_score 
    FROM exams e JOIN students s ON e.student_id = s.id 
    GROUP BY e.student_id, e.subject
''')

results_df = DataFrame(cursor.fetchall(), columns=['Name', 'Subject', 'Average Score'])

# Close the database connection
conn.close()

print(results_df)