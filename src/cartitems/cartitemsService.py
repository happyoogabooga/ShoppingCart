from db import get_db
from .cartitemsRepository import cartitemsRepository

class cartitemsService:
    def __init__(self):
        self.cartitemsRepository = cartitemsRepository(get_db())

    def getCartItems(self):
        return self.cartitemsRepository.getCartItems()

    def getCartItemsByCartsId(self, carts_id):
        return self.cartitemsRepository.getCartItemsByCartsId(carts_id)

    def getCartItemsBycartItemId(self, cartitem_id):
        return self.cartitemsRepository.getCartItemsByCartItemId(cartitem_id)

    def makeCartItem(self, carts_id, sku):
        return self.cartitemsRepository.makeCartItem(carts_id, sku)

    def removeCartItem(self, cartitem_id):
        return self.cartitemsRepository.removeCartItem(cartitem_id)

    def removeCartItemsByCartsId(self, carts_id):
        return self.cartitemsRepository.removeCartItemsByCartsId(carts_id)