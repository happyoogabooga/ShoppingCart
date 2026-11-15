from db import get_db
from .albumlistingsRepository import albumlistingsRepository

class albumlistingsService:
    def __init__(self):
        self.albumRepository = albumlistingsRepository(get_db())

    def getAlbumListings(self):
        return self.albumRepository.getAlbumListings()

    def getAlbumListingBysku(self, sku):
        return self.albumRepository.getAlbumListingBysku(sku)

    def getAlbumListingsByProviderid(self, provider_id):
        return self.albumRepository.getAlbumListingsByProviderid(provider_id)

    def makeAlbumListing(self, album_id, provider_id, price, quantity):
        return self.albumRepository.makeAlbumListing(
            album_id, provider_id, price, quantity
        )

    def deleteAlbumListing(self, sku):
        return self.albumRepository.deleteAlbumListing(sku)

    def updateAlbumListing(self, sku, album_id, provider_id, price, quantity):
        return self.albumRepository.updateAlbumListing(
            sku, album_id, provider_id, price, quantity
        )
    