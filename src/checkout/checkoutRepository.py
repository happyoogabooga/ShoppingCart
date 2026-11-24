class checkoutRepository:
    def __init__ (self, conn):
        self.conn = conn

    def getCheckouts(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM checkout"
            )
            rows = cur.fetchall()
        if rows is None:
            return None
        return [
            { "checkout_id": row[0], "user_id": row[1], "shipping_address": row[2],} for row in rows 
        ]

    def getCheckoutsByUserId(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT checkout.checkout_id, checkout.user_id, "
                "checkout.shipping_address, checkoutitems.sku, "
                "checkoutitems.title, checkoutitems.quantity, "
                "checkoutitems.unit_price "
                "FROM checkout "
                "LEFT JOIN checkoutitems "
                "ON checkoutitems.checkout_id = checkout.checkout_id "
                "WHERE checkout.user_id = %s "
                "ORDER BY checkout.checkout_id DESC, checkoutitems.sku",
                (user_id,),
            )
            rows = cur.fetchall()

        checkouts = {}
        for row in rows:
            checkout_id = row[0]
            if checkout_id not in checkouts:
                checkouts[checkout_id] = {
                    "checkout_id": checkout_id,
                    "user_id": row[1],
                    "shipping_address": row[2],
                    "items": [],
                }
            if row[3] is not None:
                checkouts[checkout_id]["items"].append({
                    "sku": row[3],
                    "title": row[4],
                    "quantity": row[5],
                    "unit_price": row[6],
                })
        return list(checkouts.values())
    def  getCheckoutsByProviderId(self, provider_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT checkout_id, user_id, shipping_address "
                "FROM checkout natural join checkoutitems join albumlistings on sku "
                "WHERE provider_id = %s", (provider_id,)
            )
            rows = cur.fetchall()
        if rows is None:
            return None

        return [{
            "checkout_id": row[0],
            "user_id": row[1],
            "shipping_address": row[2]
        }for row in rows]
    
    def getCheckoutByCheckoutId(self, checkout_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM checkout "
                "WHERE checkout_id = %s", (checkout_id,)
            )
            row = cur.fetchone()
        if row is None:
            return None
        return {
            "checkout_id": row[0],
            "user_id": row[1],
            "shipping_address": row[2]
        }

    def makeCheckoutFromUser(self, user_id, shipping_address):
        with self.conn.cursor() as cur:
            cur.execute(#get the cart
                "SELECT carts_id FROM carts "
                "WHERE user_id = %s",
                (user_id,),
            )
            cart = cur.fetchone()
            if cart is None:
                return None
            carts_id = cart[0]

            cur.execute(#return sku, title, price, and also, the amount of records with the same sku, title, and price
                "SELECT cartitem.sku, album.title, albumlistings.price, COUNT(*) "
                "FROM cartitems AS cartitem "
                "JOIN albumlistings ON albumlistings.sku = cartitem.sku "
                "JOIN album ON album.album_id = albumlistings.album_id "
                "WHERE cartitem.carts_id = %s "
                "GROUP BY cartitem.sku, album.title, albumlistings.price",
                (carts_id,),
            )
            cart_items = cur.fetchall()
            if not cart_items:
                return None

            cur.execute(#simple, now just make the checkout
                "INSERT INTO checkout (user_id, shipping_address) "
                "VALUES (%s, %s) "
                "RETURNING checkout_id, user_id, shipping_address",
                (user_id, shipping_address),
            )
            checkout = cur.fetchone()
            checkout_id = checkout[0]

            for sku, title, unit_price, quantity in cart_items:
                cur.execute(#now I simply make cart items for the checkout(gotta love python iterators)
                    "INSERT INTO checkoutitems "
                    "(checkout_id, sku, title, quantity, unit_price) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (checkout_id, sku, title, quantity, unit_price),
                )

            cur.execute( #delete the cart items
                "DELETE FROM cartitems WHERE carts_id = %s",
                (carts_id,),
            )

        self.conn.commit()
        return {
            "checkout_id": checkout[0],
            "user_id": checkout[1],
            "shipping_address": checkout[2],
        }