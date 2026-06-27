import MySQLdb

conn = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="1234",
    db="digital_library"
)

print("Connected Successfully")