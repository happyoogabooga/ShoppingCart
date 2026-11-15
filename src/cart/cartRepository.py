#this is mostly crudmuffins for now(haha crudmuffins)
class cartRepository:
    def __init__(self, conn):
        self.conn = conn

    def makeCart(self, cart_id, sku, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cart (cart_id, sku, user_id) "
                "VALUES (%s, %s, %s) "
                "RETURNING cart_id, sku, user_id",
                (cart_id, sku, user_id),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {"cart_id": row[0], "sku": row[1], "user_id": row[2]}

    def getCart(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM cart")
            rows = cur.fetchall()
        cart = [
            {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
            for row in rows]
        return cart

    def getCartById(self, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT cart_id, sku, user_id FROM cart WHERE cart_id = %s",
                (cart_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {"cart_id": row[0], "sku": row[1], "user_id": row[2]}

    def getCartByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT cart_id, sku, user_id FROM cart WHERE user_id = %s",
                (user_id,),
            )
            rows = cur.fetchall()
        return [
            {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
            for row in rows
        ]

    def updateCart(self, cart_id, sku, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE cart SET sku = %s, user_id = %s WHERE cart_id = %s "
                "RETURNING cart_id, sku, user_id",
                (sku, user_id, cart_id),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"cart_id": row[0], "sku": row[1], "user_id": row[2]}

    def deleteCart(self, cart_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cart WHERE cart_id = %s "
                "RETURNING cart_id, sku, user_id",
                (cart_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return {"cart_id": row[0], "sku": row[1], "user_id": row[2]}