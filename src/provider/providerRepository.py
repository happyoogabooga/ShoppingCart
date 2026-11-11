class providerRepository:
    def __init__(self, conn):
        self.conn = conn

    def findProviderById(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM provider WHERE provider_id = %s ", (id))
            row = cur.fetchone()
        provider = {
            "provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]
        }
        return provider

    def makeProvider(self, username, password, name):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO providor(username, password, name), VALUES (%s, %s, %s) RETURNING id, username, password, name",(username, password, name) )
            row = cur.fetchone()
        provider = {
            "provider_id":row[0], "username":row[1], "password":row[2], "name":row[3]
        }
    def getProviderByName(self, name):
        with self.conn.cursor() as cur:
            cur.execture("SELECT * FROM ")