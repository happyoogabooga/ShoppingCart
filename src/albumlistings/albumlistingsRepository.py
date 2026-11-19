class albumlistingsRepository:
    def __init__(self, conn):
        self.conn = conn

    def getAlbumListings(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * "
                "FROM albumlistings NATURAL JOIN album"
            )
            rows = cur.fetchall()
        return [
            {
                "album_id": row[0],
                "sku": row[1],
                "provider_id": row[2],
                "price": row[3],
                "quantity": row[4],
                "title": row[5],
                "description": row[6],
                "image": row[7],
                "artist": row[8]
            }
            for row in rows
        ]

    def getAlbumListingBysku(self, sku):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * "
                "FROM albumlistings NATURAL JOIN album WHERE sku = %s",
                (sku,)
            )
            row = cur.fetchone()
        return {
                "album_id": row[0],
                "sku": row[1],
                "provider_id": row[2],
                "price": row[3],
                "quantity": row[4],
                "title": row[5],
                "description": row[6],
                "image": row[7],
                "artist": row[8]
            }
        
        
    def getAlbumListingsByProviderid(self, provider_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * "
                "FROM albumlistings NATURAL JOIN album WHERE provider_id = %s",
                (provider_id,),
            )
            rows = cur.fetchall()
        return [
            {
                "album_id": row[0],
                "sku": row[1],
                "provider_id": row[2],
                "price": row[3],
                "quantity": row[4],
                "title": row[5],
                "description": row[6],
                "image": row[7],
                "artist": row[8]
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
    #I need to make sure that this deletion is consistent throughtout the database
    def deleteAlbumListing(self, sku):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cart WHERE sku = %s",
                (sku,),
            )
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