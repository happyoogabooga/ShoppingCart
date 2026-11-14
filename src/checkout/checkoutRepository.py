class checkoutRepository:
    def __init__(self, conn):
        self.conn = conn

    def makeCheckout(self, user_id, total_amount, cart_id):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO checkout (user_id, total_amount, cart_id) VALUES (%s, %s, %s)",(user_id, total_amount, cart_id))
            row = cur.fetchone()
        checkout = {
            "order_number": row[0], "user_id": row[1], "total_amount": row[2], "cart_id": row[3]
        }
        return checkout
    
    def getCheckoutByCartId(self, cart_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM checkout WHERE cart_id = %s", (cart_id))
            row = cur.fetchone()
        checkout = {
            "order_number": row[0], "user_id": row[1], "total_amount": row[2], "cart_id": row[3]
        }
        return checkout
    
    def getCheckoutByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM checkout WHERE user_id = %s", (user_id))
            row = cur.fetchone
        checkout = {
            "order_number": row[0], "user_id": row[1], "total_amount": row[2], "cart_id": row[3]
        }
        return checkout