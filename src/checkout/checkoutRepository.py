class checkoutRepository:
    def __init__(self, conn):
        self.conn = conn

    def makeCheckout(self, user_id, total_amount, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO checkout (user_id, total_amount, cart_id) "
                "VALUES (%s, %s, %s) "
                "RETURNING order_number, user_id, total_amount, cart_id",
                (user_id, total_amount, cart_id),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {
            "order_number": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "cart_id": row[3],
        }

    def getCheckoutByCartId(self, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT order_number, user_id, total_amount, cart_id "
                "FROM checkout WHERE cart_id = %s",
                (cart_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "order_number": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "cart_id": row[3],
        }
    
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

    def getCheckoutById(self, order_number):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT order_number, user_id, total_amount, cart_id "
                "FROM checkout WHERE order_number = %s",
                (order_number,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "order_number": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "cart_id": row[3],
        }

    def updateCheckout(self, order_number, user_id, total_amount, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE checkout SET user_id = %s, total_amount = %s, cart_id = %s "
                "WHERE order_number = %s "
                "RETURNING order_number, user_id, total_amount, cart_id",
                (user_id, total_amount, cart_id, order_number),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "order_number": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "cart_id": row[3],
        }

    def deleteCheckout(self, order_number):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM checkout WHERE order_number = %s "
                "RETURNING order_number, user_id, total_amount, cart_id",
                (order_number,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {
            "order_number": row[0],
            "user_id": row[1],
            "total_amount": row[2],
            "cart_id": row[3],
        }