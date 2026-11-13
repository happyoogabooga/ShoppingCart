class albumRepository:
    def __init__(self, conn):
        self.conn = conn

    def getAlbumById(self, id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM album WHERE album_id = %s", (id))
            row = cur.fetchone
        album = {
            {"album_id": row[0], "title": row[1], "description": row[2], "image": row[3], "artist": row[4]}
        }
        return album
    
    def findAllAlbums(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT album_id, title, description, image, artist FROM album ORDER BY album_id")
            rows = cur.fetchall()
        albums = [
            {"album_id": row[0], "title": row[1], "description": row[2], "image": row[3], "artist": row[4]}
            for row in rows
        ]
        return albums
    
    def findAlbumByName(self, name):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM album WHERE title like 'name%' ")
            rows = cur.fetchall()
        albums = [
            {"album_id": row[0], "title": row[1], "description": row[2], "image": row[3], "artist": row[4]}
            for row in rows
        ]
        return albums
        

    def findAlbumByArtist(self, artist):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM album WHERE artist like '%s%' ", (artist))
            rows = cur.fetchall()
        albums = [
            {"album_id": row[0], "title": row[1], "description": row[2], "image": row[3], "artist": row[4]}
            for row in rows
        ]
        return albums
    
    #do note, uploading the album technically does not require me to go and get all of my provider information, I am simply passing the provider ID into the querry
    def makeAlbum(self, title, description, image, artist):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO album (title, description, image, artist ) VALUES (%s, %s, %s, %s) RETURNING album_id, title, description, image, artist;",
                (title, description, image, artist)
            )
            row = cur.fetchone()
        self.conn.commit()
        return{
            "id": row[0],
            "title": row[1],
            "artist": row[2],
            "price": row[3]
        }