from db import get_db
from .cartsRepository import cartsRepository

class cartsService:
    def __init__(self):
        self.cartsRepository = cartsRepository(get_db())
    def getCarts(self):
        return self.cartsRepository.getCarts()
    
    def getCartsByCartsId(self, carts_id):
        return self.cartsRepository.getCartsByCartsId(carts_id)

    def getCartsByUserId(self, user_id):
        return self.cartsRepository.getCartsByUserId(user_id)
        
    def makeCarts(self, user_id):
        return self.cartsRepository.makeCart(user_id)

    def removeCarts(self, carts_id):
        return self.cartsRepository.removeCart(carts_id)