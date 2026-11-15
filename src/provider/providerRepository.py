class providerRepository:
    def __init__(self, conn):
        self.conn = conn

    def getProviderById(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT provider_id, username, name "
                "FROM provider WHERE provider_id = %s",
                (id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {"provider_id": row[0], "username": row[1], "name": row[2]}

    def makeProvider(self, username, password, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO provider (username, password, name) "
                "VALUES (%s, %s, %s) "
                "RETURNING provider_id, username, name",
                (username, password, name),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {"provider_id": row[0], "username": row[1], "name": row[2]}
    def getProviderByName(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT provider_id, username, name "
                "FROM provider WHERE name ILIKE %s",
                (f"%{name}%",),
            )
            rows = cur.fetchall()
        return [
            {"provider_id": row[0], "username": row[1], "name": row[2]}
            for row in rows
        ]

    def updateProvider(self, id, username, password, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE provider SET username = %s, password = %s, name = %s "
                "WHERE provider_id = %s "
                "RETURNING provider_id, username, name",
                (username, password, name, id),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"provider_id": row[0], "username": row[1], "name": row[2]}

    def deleteProvider(self, provider_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM provider WHERE provider_id = %s "
                "RETURNING provider_id, username, name",
                (provider_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"provider_id": row[0], "username": row[1], "name": row[2]}

    def getProviders(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT provider_id, username, name FROM provider")
            rows = cur.fetchall()
        return [
            {"provider_id": row[0], "username": row[1], "name": row[2]}
            for row in rows
        ]