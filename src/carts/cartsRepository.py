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
        } for row in rows ]
    
    def getCartsByCartsId(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM carts WHERE carts_id = %s", (carts_id)
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
                "SELECT * FROM carts WHERE user_id = %s", (user_id)
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
                "INSERT INTO carts (user_id)"
                "VALUES (%s)"
                "RETURNING(carts_id, user_id)",(user_id),
            )
            row = cur.fetchone()
        self.conn.commit()
        return {
            "carts_id": row[0],
            "user_id": row[1]
        }
    
    def removeCart(self, carts_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM carts WHERE carts_id = %s"
                "RETURNING carts_id, user_id",(carts_id),
            )
            row = cur.fetchone()
        if row is None:
            return None
        self.conn.commit()
        return{
            "carts_id": row[0],
            "user_id": row[1]
        }