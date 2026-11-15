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
    
    def getCheckoutsByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT order_number, user_id, total_amount, cart_id "
                "FROM checkout WHERE user_id = %s ORDER BY order_number",
                (user_id,),
            )
            rows = cur.fetchall()
        return [
            {
                "order_number": row[0],
                "user_id": row[1],
                "total_amount": row[2],
                "cart_id": row[3],
            }
            for row in rows
        ]

    def updateCheckout(self, order_number, user_id, total_amount, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE checkout set user_id = %s, total_amount = %s, cart_id = %s WHERE order_number = %s",
                (user_id, total_amount, cart_id, order_number)
            )
            row = cur.fetchone()
        checkout = {
            "order_number": row[0], "user_id": row[1], "total_amount": row[2], "cart_id": row[3]
        }
        return checkout

    def deleteCheckout(self, order_number):
        with self.conn.cursor() as cur:
            cur.exectue(
                "DELETE FROM checkout WHERE order_number = %s",
                (order_number)
            )
            row = cur.fetchone()
        checkout = {
            "order_number": row[0], "user_id": row[1], "total_amount": row[2], "cart_id": row[3]
        }
        return checkout