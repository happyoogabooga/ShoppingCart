class albumlistingsRepository:
    def __init__(self, conn):
        self.conn = conn

    def getAlbumListings(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM albumlistings")
            rows = cur.fetchall()
        albumlistings = [{
            "sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]
        } for row in rows]
        return albumlistings

    def getAlbumListingBysku(self, sku):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT sku, album_id, provider_id, price, quantity "
                "FROM albumlistings WHERE sku = %s",
                (sku,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "sku": row[0],
            "album_id": row[1],
            "provider_id": row[2],
            "price": row[3],
            "quantity": row[4],
        }
        
    def getAlbumListingsByProviderid(self, provider_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT sku, album_id, provider_id, price, quantity "
                "FROM albumlistings WHERE provider_id = %s",
                (provider_id,),
            )
            rows = cur.fetchall()
        return [
            {
                "sku": row[0],
                "album_id": row[1],
                "provider_id": row[2],
                "price": row[3],
                "quantity": row[4],
            }
            for row in rows
        ]
    
    #i want to return all albums of like-names, how to do this?
    def makeAlbumListing(self, album_id, provider_id, price, quantity):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO albumlistings (album_id, provider_id, price, quantity) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING sku, album_id, provider_id, price, quantity",
                (album_id, provider_id, price, quantity),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {
            "sku": row[0],
            "album_id": row[1],
            "provider_id": row[2],
            "price": row[3],
            "quantity": row[4],
        }

    def deleteAlbumListing(self, sku):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM albumlistings WHERE sku = %s "
                "RETURNING sku, album_id, provider_id, price, quantity",
                (sku,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "sku": row[0],
            "album_id": row[1],
            "provider_id": row[2],
            "price": row[3],
            "quantity": row[4],
        }

    def updateAlbumListing(self, sku, album_id, provider_id, price, quantity):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE albumlistings "
                "SET album_id = %s, provider_id = %s, price = %s, quantity = %s "
                "WHERE sku = %s "
                "RETURNING sku, album_id, provider_id, price, quantity",
                (album_id, provider_id, price, quantity, sku),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "sku": row[0],
            "album_id": row[1],
            "provider_id": row[2],
            "price": row[3],
            "quantity": row[4],
        }