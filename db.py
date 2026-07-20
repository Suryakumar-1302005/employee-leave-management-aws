import pymysql

def get_connection():
    return pymysql.connect(
        host="leavedb.crwek2okyy3g.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="leavedb",
        autocommit=True
    )