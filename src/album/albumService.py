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
        return self.album_repository.findAlbumByName(title)

    def makeAlbum(self, title, description, image, artist):
        return self.album_repository.makeAlbum(title, description, image, artist)
    
    def getAlbumById(self, id):
        return self.album_repository.getAlbumById(id)