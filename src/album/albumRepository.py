class albumRepository:
    def __init__(self, conn):
        self.conn = conn

    def getAlbumById(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT album_id, title, description, image, artist "
                "FROM album WHERE album_id = %s",
                (id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "album_id": row[0],
            "title": row[1],
            "description": row[2],
            "image": row[3],
            "artist": row[4],
        }
    
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
            cur.execute(
                "SELECT album_id, title, description, image, artist "
                "FROM album WHERE title ILIKE %s",
                (f"%{name}%",),
            )
            rows = cur.fetchall()
        albums = [
            {"album_id": row[0], "title": row[1], "description": row[2], "image": row[3], "artist": row[4]}
            for row in rows
        ]
        return albums
        

    def findAlbumByArtist(self, artist):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT album_id, title, description, image, artist "
                "FROM album WHERE artist ILIKE %s",
                (f"%{artist}%",),
            )
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
                "INSERT INTO album (title, description, image, artist) "
                "VALUES (%s, %s, %s, %s) "
                "RETURNING album_id, title, description, image, artist",
                (title, description, image, artist),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {
            "album_id": row[0],
            "title": row[1],
            "description": row[2],
            "image": row[3],
            "artist": row[4],
        }

    def updateAlbum(self, album_id, title, description, image, artist):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE album SET title = %s, description = %s, image = %s, artist = %s "
                "WHERE album_id = %s "
                "RETURNING album_id, title, description, image, artist",
                (title, description, image, artist, album_id),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "album_id": row[0],
            "title": row[1],
            "description": row[2],
            "image": row[3],
            "artist": row[4],
        }

    def removeAlbum(self, album_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM album WHERE album_id = %s "
                "RETURNING album_id, title, description, image, artist",
                (album_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "album_id": row[0],
            "title": row[1],
            "description": row[2],
            "image": row[3],
            "artist": row[4],
        }