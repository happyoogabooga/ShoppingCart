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

    def getCheckoutById(self, order_number):
        return self.checkoutRepository.getCheckoutById(order_number)

    def updateCheckout(self, order_number, user_id, total_amount, cart_id):
        return self.checkoutRepository.updateCheckout(
            order_number, user_id, total_amount, cart_id
        )

    def deleteCheckout(self, order_number):
        return self.checkoutRepository.deleteCheckout(order_number)