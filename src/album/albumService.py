from db import get_db
from .albumRepository import albumRepository


class AlbumService:
    def __init__(self):
        self.album_repository = albumRepository(get_db())

    def getAlbums(self):
        return self.album_repository.findAllAlbums()

    def getAlbumArtist(self, name):
        return self.album_repository.findAlbumByArtist(name=name)

    def findBytitle(self, title):
        return self.album_repository.findAlbumByName(name=title)

    def postAlbum(self, title, artist, price):
        return self.album_repository.uploadAlbum(title, artist, price)
