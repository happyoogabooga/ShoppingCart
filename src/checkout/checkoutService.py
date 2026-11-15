from db import get_db
from .checkoutRepository import checkoutRepository
class checkoutService:
    def __init__(self):
        self.checkoutRepository = checkoutRepository(get_db())

    def makeCheckout(self, user_id, total_amount, cart_id):
        return self.checkoutRepository.makeCheckout(user_id, total_amount, cart_id)

    def getCheckoutByCartId(self, cart_id):
        return self.checkoutRepository.getCheckoutByCartId(cart_id)

    def getCheckoutsByUserId(self, user_id):
        return self.checkoutRepository.getCheckoutsByUserId(user_id)