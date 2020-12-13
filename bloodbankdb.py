import pymysql
conn=pymysql.connect(
                    host='sql12.freemysqlhosting.net',
                    database='sql12375682',
                    user='sql12375682',
                    password='nL9hwqHpV7',
                    cursorclass=pymysql.cursors.DictCursor
                    )  
cursor=conn.cursor()
query="""CREATE TABLE IF NOT EXISTS blood(id INTEGER AUTO_INCREMENT PRIMARY KEY,
                                          name VARCHAR(25) NOT NULL,
                                          location VARCHAR(20) NOT NULL,
                                          email VARCHAR(20) NOT NULL,
                                          gender VARCHAR(10) NOT NULL,
                                          mobileno  INTEGER NOT NULL,
                                          bloodgroup VARCHAR(10) NOT NULL
)"""
cursor.execute(query)                                          
conn.close()


