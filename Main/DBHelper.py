import mysql.connector

config = {
    "user":"root",
    "password":"root",
    "host":"127.0.0.1",
    "database":"aidouban",
}

def getconn():
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(err)
        return None
    print("Success")
    return cnx.cursor(buffered=True)


def insertMovieInfo():
    pass

if __name__ == '__main__':
    getconn()