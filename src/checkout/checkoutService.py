from db import get_db
from .checkoutRepository import checkoutRepository
class checkoutService:
    def __init__(self):
        self.checkoutRepository = checkoutRepository(get_db())

    def getCheckouts(self):
        return self.checkoutRepository.getCheckouts()

    def getCheckoutsByUserId(self, user_id):
        return self.checkoutRepository.getCheckoutsByUserId(user_id)

    def getCheckoutsByProviderId(self, provider_id):
        return self.checkoutRepository.getCheckoutsByProviderId(provider_id)

    def getCheckoutByCheckoutId(self, checkout_id):
        return self.checkoutRepository.getCheckoutByCheckoutId(checkout_id)

    def makeCheckout(self, user_id, shipping_address):
        return self.checkoutRepository.makeCheckoutFromUser(
            user_id,
            shipping_address,
        )