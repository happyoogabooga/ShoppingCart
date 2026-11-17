class usersRepository:
    def __init__(self, conn):
        self.conn = conn

    def findUserById(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, location FROM users WHERE user_id = %s",
                (id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "user_id": row[0],
            "username": row[1],
            "location": row[2],
        }

    def findUserByCredentials(self, username, password):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, location FROM users "
                "WHERE username = %s AND password = %s",
                (username, password),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "user_id": row[0],
            "username": row[1],
            "location": row[2],
        }

    def makeUser(self, username, password, location, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password, location, name) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING user_id, username, location, name",
                (username, password, location, name),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {"user_id": row[0], "username": row[1], "location": row[2], "name": row[3]}
    
    def getUsers(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT user_id, username, location FROM users")
            rows = cur.fetchall()
        users = [
            {"user_id": row[0], "username": row[1], "location": row[2], "name": row[3]}
            for row in rows
        ]
        return users

    def updateUser(self, user_id, username, password, location, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET username = %s, password = %s, location = %s, name = %s "
                "WHERE user_id = %s "
                "RETURNING user_id, username, location, name",
                (username, password, location, name, user_id),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"user_id": row[0], "username": row[1], "location": row[2], "name": row[3]}

    def deleteUser(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE user_id = %s "
                "RETURNING user_id, username, location",
                (user_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"user_id": row[0], "username": row[1], "location": row[2]}