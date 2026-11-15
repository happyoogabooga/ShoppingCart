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

    def getAlbumListingBysku(self, sku):#this is the specific album, not a collection of albums, could be useful for putting an album in a cart
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM albumlistings where sku = %s", (sku))
            row = cur.fetchone()
        albumlisting = {"sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]}
        return albumlisting
        
    def getAlbumListingsByProviderid(self, provider_id): #get the albums a provider is selling
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM albumlistings where provider_id = %s", (provider_id))
            row = cur.fetchone()
        albumlisting = {"sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]}
        return albumlisting
    
    #i want to return all albums of like-names, how to do this?
    def makeAlbumListing(self, album_id, provider_id, price, quantity):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO albumlistings(album_id, provider_id, price, quantity) Values (%s, %s, %s, %s)", (album_id, provider_id, price, quantity))
            row = cur.fetchone()
        albumlisting = {"sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]}
        return albumlisting

    def deleteAlbumListing(self, sku):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM albumlistings WHERE sku = %s", (sku))
            row = cur.fetchone()
        albumlisting = {"sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]}
        return albumlisting

    def updateAlbumListing(self, sku, album_id, provider_id, price, quantity):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE albumListings SET album_id = %s, provider_id = %s, price = %s, quantity = %s WHERE sku = %s", (album_id, provider_id, price, quantity, sku))
            row = cur.fetchone()
        albumlisting = {"sku": row[0], "album_id": row[1], "provider_id": row[2], "price": row[3], "quantity": row[4]}
        return albumlisting