import sqlite3

# Connect to the database
conn = sqlite3.connect('recruitment.db')
cursor = conn.cursor()

# Query all emails from the candidates table
cursor.execute('SELECT id ,email FROM candidates')
emails = cursor.fetchall()
cursor.execute('SELECT id, title FROM job_descriptions')
jobs = cursor.fetchall()

# Print job ID & title
print("Job ID & Title")
for job in jobs:
    print(f"{job[0]} & {job[1]}") 
# Print the emails
print("Emails in the candidates table:")
for email in emails:
    print(f"{email[0]} & {email[1]}")  # email[0] accesses the first (and only) column

# Close the connection
conn.close()