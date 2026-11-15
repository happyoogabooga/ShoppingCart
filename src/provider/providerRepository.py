class providerRepository:
    def __init__(self, conn):
        self.conn = conn

    def getProviderById(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM provider WHERE provider_id = %s ", (id))
            row = cur.fetchone()
        provider = {
            "provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]
        }
        return provider

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
            cur.execute("SELECT * FROM provider WHERE name like %s%", (name))
            rows = cur.fetchall()
        provider = [
            {"provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]}
            for row in rows
        ]
        return provider
    #here I update the provider with this id, I can update the username password and name
    def updateProvider(self, id, username, password, name):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE provider SET username = %s, password = %s, name = %s WHERE provider_id = %s", (username, password, name, id))
            row = cur.fetchone
        provider = {
            "provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]
        }
        return provider

    def getProviders(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM provider")
            rows = cur.fetchall()
        provider = [{"provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]} for row in rows]
        return provider
    #this makes a whole nother problem with keeping persistance between albums and the provider as, if the provider is deleted, the albums associated with that provider should also be deleted
    #!!!!!!!!!!MAKE SURE TO TAKE CARE OF THIS ISSUE IN THE SERVICE!!!!!!!!
    #def deleteProvidor()