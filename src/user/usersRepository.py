class usersRepository:
    def __init__(self, conn):
        self.conn = conn

    def findUserById(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, password, location FROM users WHERE user_id = %s",
                (id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "user_id": row[0],
            "username": row[1],
            "password": row[2],
            "location": row[3],
        }

    def makeUser(self, username, password, location):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password, location) "
                "VALUES (%s, %s, %s) "
                "RETURNING user_id, username, location",
                (username, password, location),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {"user_id": row[0], "username": row[1], "location": row[2]}
    
    def getUsers(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM USERS"
            )
            rows = cur.fetchall()
        users = [
            {"user_id": row[0], "username": row[1], "password": row[2], "location": row[3]}
            for row in rows
        ]
        return users

    def updateUser(self, user_id, username, password, location):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET username = %s, password = %s, location = %s, WHERE user_id = %s",
                (username, password, location, user_id)
            )
            row = cur.fetchone()
        users = {
            "user_id": row[0], "username": row[1], "password": row[2], "location": row[3]
            }
        return users

    def deleteUser(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE user_id =%s", 
                (user_id)
            )
            row = cur.fetchone()
        users = {
            "user_id": row[0], "username": row[1], "password": row[2], "location": row[3]
            }
        return users