from db import get_db
from .albumlistingsRepository import albumlistingsRepository

class albumlistingsService:
    def __init__(self):
        self.albumRepository = albumlistingsRepository(get_db)

    def getAlbumListings(self):
        return self.albumRepository.getAlbumListings()

    def getAlbumListingBysku(self, sku):
        return self.albumRepository.getAlbumListingBysku(sku)

    def getAlbumListingsByProviderid(self, provider_id):
        return self.getAlbumListingBysku(provider_id)

    def makeAlbumListing(self, album_id, provider_id, price, quantity):
        return self.makeAlbumListing(album_id, provider_id, price, quantity)

    def deleteAlbumListing(self, sku):
        return self.deleteAlbumListing(sku)

    def updateAlbumListing(self, sku, album_id, provider_id, price, quantity):
        return self.updateAlbumListing(sku, album_id, provider_id, price, quantity)
    