#this is mostly crudmuffins for now(haha crudmuffins)
class cartRepository:
    def __init__(self, conn):
        self.conn = conn

    def makeCart(self, sku, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cart (sku, user_id) "
                "VALUES (%s, %s) "
                "ON CONFLICT (user_id, sku) "
                "DO UPDATE SET cart_quantity = cart.cart_quantity + 1 "
                "RETURNING cart_id, sku, user_id",
                (sku, user_id),
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
    
    def getItemsByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT sku, cart_id, user_id, cart_quantity, A.album_id, provider_id, price, title, description, image, artist " \
                "FROM cart NATURAL JOIN albumlistings AS A JOIN album AS B ON A.album_id = B.album_id "\
                "WHERE user_id = %s",
                (user_id,),
            )
            rows = cur.fetchall()
        return [
            {"sku": row[0], "cart_id": row[1], "user_id": row[2], "cart_quantity": row[3], "album_id": row[4], "provider_id": row[5], "price": row[6], "title": row[7], "description": row[8], "image": row[9], "artist": row[10]}
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
                "UPDATE cart SET cart_quantity = cart_quantity - 1 "
                "WHERE cart_id = %s AND cart_quantity > 1 "
                "RETURNING cart_id, sku, user_id",
                (cart_id,),
            ) 
            row = cur.fetchone()
            if row is None:
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
        