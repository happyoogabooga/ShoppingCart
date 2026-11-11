class albumRepository:
    def __init__(self, conn):
        self.conn = conn

    def findAllAlbums(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT SKU, description, title, artist, price FROM album ORDER BY SKU")
            rows = cur.fetchall()
        albums = [
            {"SKU": row[0], "description": row[1], "title": row[2], "artist": row[3], "price": row[4]}
            for row in rows
        ]
        return albums
    
    def findAlbumByName(self, name):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM album WHERE title like 'name%' ")
            rows = cur.fetchall()
        albums = [
            {"id": row[0], "title": row[1], "artist": row[2], "price": row[3]}
            for row in rows
        ]
        return albums
        

    def findAlbumByArtist(self, artist):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM album WHERE artist like 'artist%' ")
            rows = cur.fetchall()
        albums = [
            {"id": row[0], "title": row[1], "artist": row[2], "price": row[3]}
            for row in rows
        ]
        return albums
#note, this is a terrible thing to test on, something that doesnt require a foreign key would be better
    def uploadAlbum(self, SKU, title, description, artist, price):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO album (title, artist, price) VALUES (%s, %s, %s) RETURNING id, title, artist, price;",
                (title, artist, price)
            )
            row = cur.fetchone()
        self.conn.commit()
        return{
            "id": row[0],
            "title": row[1],
            "artist": row[2],
            "price": row[3]
        }