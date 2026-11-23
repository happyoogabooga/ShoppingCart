from ..albumlistings.albumlistingsSerivce import albumlistingsService
class cartitemsRepository:
    def __init__(self, conn):
        self.conn = conn

    def getCartItems(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT cartitem_id, carts_id, sku FROM cartitems"
            )
            rows = cur.fetchall()
        return[
            {"cartitem_id": row[0],
             "carts_id": row[1],
             "sku": row[2]}
             for row in rows
        ]

    def getCartItemsByCartsId(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT cartitem_id, carts_id, sku FROM cartitems "
                "WHERE carts_id = %s",
                (carts_id,),
            )
            rows = cur.fetchall()
        return[
            {"cartitem_id": row[0],
             "carts_id": row[1],
             "sku": row[2]}
             for row in rows
        ]

    def getCartItemsByCartItemId(self, cartitem_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT cartitem_id, carts_id, sku FROM cartitems "
                "WHERE cartitem_id = %s",
                (cartitem_id,),
            )
            row = cur.fetchone()
        if row is None:
            return None
        return{"cartitem_id": row[0],
               "carts_id": row[1],
               "sku":row[2]
             }

    def makeCartItem(self, carts_id, sku):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cartitems (carts_id, sku) "
                "VALUES (%s, %s) "
                "RETURNING cartitem_id, carts_id, sku",
                (carts_id, sku),
            )
            #thinking of what I need to do, it would be valuable to get the quantity of the album listings first, and then do this update, here goes
            row = cur.fetchone()
            #count the items in cartItem with the same sku
            cur.execute(
                "SELECT count(sku)"
                "FROM cartitems"
                "WHERE sku = %s",(sku),
            )
            currentquantity = cur.fetchone()

        self.conn.commit()
        if row is None:
            return None
         currentquantity[0]
        return {
            "cartitem_id": row[0],
            "carts_id": row[1],
            "sku": row[2]
        }

    def removeCartItem(self, cartitem_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cartitems "
                "WHERE cartitem_id = %s "
                "RETURNING cartitem_id, carts_id, sku",
                (cartitem_id,),
            )
            row = cur.fetchone()
        self.conn.commit()
        if row is None:
            return None
        return {
            "cartitem_id": row[0],
            "carts_id": row[1],
            "sku": row[2]
        }

    def removeCartItemsByCartsId(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM cartitems "
                "WHERE carts_id = %s "
                "RETURNING cartitem_id, carts_id, sku",
                (carts_id,),
            )
            rows = cur.fetchall()
        self.conn.commit()
        if rows is None:
            return None
        return[{
            "cartitem_id": row[0],
            "carts_id": row[1],
            "sku": row[2]
        }for row in rows]