import pandas as pd
import sqlite3

conn = sqlite3.connect('attendance.db')
attendance_df = pd.read_sql_query("SELECT * FROM attendance", conn)
conn.close()

attendance_df.to_csv('attendance_report.csv', index=False)
print("Attendance report saved as attendance_report.csv")
