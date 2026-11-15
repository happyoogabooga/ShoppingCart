#this is mostly crudmuffins for now(haha crudmuffins)
class cartRepository:
    def __init__(self, conn):
        self.conn = conn

    def makeCart(self, cart_id, sku, user_id):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO cart(cart_id, sku, user_id) VALUES (%s, %s, %s)", (cart_id, sku, user_id))
            row = cur.fetchone()
        cart = {
            "user_id": row[0], "sku":row[1]
        }
        return cart

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
            cur.execute("SELECT * FROM cart WHERE cart_id = %s", (cart_id))
            row = cur.fetchone()
        cart = {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
        return cart

    def getCartByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM cart WHERE user_id = %s", (user_id))
            row = cur.fetchone()
        cart = {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
        return cart

    def updateCart(self, cart_id, sku, user_id):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE cart set sku = %s, user_id = %s WHERE cart_id = %s", (sku, user_id, cart_id))
            row = cur.fetchone()
        cart = {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
        return cart

    def deleteCart(self, cart_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM cart WHERE cart_id = %s", (cart_id))
            row = cur.fetchone()
        cart = {"cart_id": row[0], "sku": row[1], "user_id": row[2]}
        return cart