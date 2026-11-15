from db import get_db
from .cartRepository import cartRepository

class cartService:
    def __init__(self):
        self.cartRepository = cartRepository(get_db())

    def makeCart(self, cart_id, sku, user_id):
        return self.cartRepository.makeCart(cart_id, sku, user_id)
    
    def getCart(self):
        return self.cartRepository.getCart()

    def getCartById(self, cart_id):
        return self.cartRepository.getCartById(cart_id)

    def getCartByUserId(self, user_id):
        return self.cartRepository.getCartByUserId(user_id)

    def updateCart(self, cart_id, sku, user_id):
        return self.cartRepository.updateCart(cart_id, sku, user_id)

    def removeCart(self, cart_id):
        return self.cartRepository.deleteCart(cart_id)
    