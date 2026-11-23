class cartsRepository:
    def __init__(self, conn):
        self.conn = conn

    def getCarts(self):
        with self.conn.cursor() as cur:
            cur.excute(
                "SELECT * FROM CARTS"
            )
            rows = cur.fetchall()
        return [{
            "carts_id": row[0],
            "user_id": row[1]
        } for row in rows]
    
    def getCartsByCartsId(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT carts_id, user_id FROM carts WHERE carts_id = %s",
                (carts_id,),
            )
            row = cur.fetchone()

        if row is None:
            return None
        
        return {
            "carts_id": row[0],
            "user_id": row[1]
        }
    
    def getCartsByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT carts_id, user_id FROM carts WHERE user_id = %s",
                (user_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return{
            "carts_id": row[0],
            "user_id": row[1]
        }
    
    def makeCart(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO carts (user_id) "
                "VALUES (%s) "
                "ON CONFLICT (user_id) DO UPDATE SET user_id = EXCLUDED.user_id "
                "RETURNING carts_id, user_id",
                (user_id,),
            )
            row = cur.fetchone()
        self.conn.commit()
        if row is None:
            return None
        return {
            "carts_id": row[0],
            "user_id": row[1]
        }
    
    def getCartItemsAndSkuByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT sku, cartitem_id, carts.carts_id, album_id, provider_id, price, quantity, user_id"
                "FROM cartitems natural join albumlistings join carts on cartitems.carts_id = carts.carts_id"
                "WHERE user_id = %s",(user_id)
            )
            row = cur.fetchall()
        if row is None:
            return None
        return{
            "sku": row[0],
            "cartitem_id": row[1],
            "carts.carts_id": row[2],
            "album_id": row[3],
            "provider_id": row[4],
            "price": row[5],
            "quantity": row[6],
            "user_id": row[7]
        }
    def removeCart(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cartitems WHERE carts_id = %s",
                (carts_id,),
            )
            cur.execute(
                "DELETE FROM carts WHERE carts_id = %s "
                "RETURNING carts_id, user_id",
                (carts_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return{
            "carts_id": row[0],
            "user_id": row[1]
        }
    