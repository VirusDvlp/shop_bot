from pymysql import connect
from pymysql.cursors import DictCursor



class DataBase:


    def __init__(self) -> None:
        self.con = connect(
            host='localhost',
            user='root',
            password='Bobrdobr12!',
            database='shop_bot',
            port=3306,
            cursorclass=DictCursor
        )


    def add_user(self, user_id, username, name) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `users` (`user_id`, `username`, `name`) VALUES(%s, %s, %s)',
                (user_id, username, name)
            )
            self.save()


    def check_user_exist(self, user_id) -> bool:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `id` FROM `users` WHERE `user_id` = %s',
                (user_id,)
            )
            return cur.fetchone()


    def get_user_data(self, user_id):
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `username`, `name` FROM `users` WHERE `user_id` = %s',
                (user_id,)
            )
            return cur.fetchone()


    def get_users(self) -> tuple:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `user_id` FROM `users`'
            )
            return cur.fetchall()
        

    def set_user_basket(self, user_id, basket) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                'UPDATE `users` SET `basket` = %s WHERE `user_id` = %s',
                (basket, user_id)
            )
            self.save()

    def get_user_basket(self, user_id) -> list:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `basket` FROM `users` WHERE `user_id` = %s',
                (user_id,)
            )
            return cur.fetchone()['basket'].split(',')



    def clear_user_basket(self, user_id) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                'UPDATE `users` SET `basket` = \'\' WHERE `user_id` = %s',
                (user_id,)
            )
            self.save()


    def add_good(self, name, descr, price, category, image) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `goods` (name, descr, price, category, image) VALUES (%s, %s, %s,  %s, %s)',
                (name, descr, price, category, image)
            ),
            self.save()


    def edit_good_data(self, key, value, id) -> None:
        with self.con.cursor() as cur:
            cur.execute(f'UPDATE `goods` SET {key} = {value} WHERE `id` = {id}')
            self.save()


    def add_category(self, name) -> None:
        with self.con.cursor() as cur:
            cur.execute(
                'INSERT INTO `categories` (name) VALUES(%s)',
                (name)
            )
            self.save()


    def get_list_of_categories(self) -> tuple:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT * FROM `categories`'
            )
            return cur.fetchall()


    def get_list_of_goods(self, category):
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `id`, `price`, `name`, `descr`, `image`, `available` FROM `goods` WHERE `category` = %s',
                (category,)
            )
            return cur.fetchall()
        

    def get_good_price(self, good_id) -> int:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `price` FROM `goods` WHERE `id` = %s',
                (good_id,)
            )
            return int(cur.fetchone()['price'])
        

    def get_good_data(self, good_id) -> dict:
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `price`, `name` FROM `goods` WHERE `id` = %s',
                (good_id,)
            )
            return cur.fetchone()


    def get_goods_by_search(self, search) -> tuple:
        with self.con.cursor() as cur:
            search = '%' + search + '%'
            cur.execute(
                '''SELECT `id`, `price`, `name`, `descr`, `image`, `available` FROM `goods`'
                WHERE LOWER(name) LIKE %s OR LOWER(descr) LIKE %s''',
                (search, search)
            )
            return cur.fetchall()



    def add_order_request(self, user_id, basket, lat, lon, gt, pay_type, total) -> int:
        with self.con.cursor() as cur:
            cur.execute(
                '''INSERT INTO `orders` (`user_id`, `basket`, `lat`, `lon`, `get_type`, `pay_type`, `total`)'
                VALUES(%s, %s, %s, %s, %s, %s, %s)''',
                (user_id, basket, lat, lon, gt, pay_type, total)
            )
            self.save()
            cur.execute(
                'SELECT `id` FROM `orders` WHERE `user_id` = %s ORDER BY `user_id` DESC',
                (user_id,)
            )
            return cur.fetchone()['id']


    def get_order_status(self, order_id):
        with self.con.cursor() as cur:
            cur.execute(
                'SELECT `status` FROM `orders` WHERE `id` = %s',
                (order_id,)
            )
            return cur.fetchone()['status']


    def set_order_status(self, order_id, status):
        with self.con.cursor() as cur:
            cur.execute(
                'UPDATE `orders` SET `status` = %s WHERE `id` = %s',
                (status, order_id)
            )
            self.save()
        

    def get_order_data(self, order_id):
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT orders.user_id, `status`, `pay_type`, orders.basket, `lat`, `lon`, `get_type`, `date`, users.name,
                users.username, `total` FROM `orders` JOIN `users` ON orders.user_id = users.user_id WHERE orders.id = %s''',
                (order_id,)
            )
            return cur.fetchone()
        

    def get_orders_by_status_and_user(self, status, user):
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT `id`, `date`, `basket` FROM `orders` WHERE `status` = %s AND `user_id` = %s''',
                (status, user)
            )
            return cur.fetchall()
        

    def get_orders_by_status(self, status):
        with self.con.cursor() as cur:
            cur.execute(
                '''SELECT orders.id, `date`, users.username FROM `orders` JOIN `users` ON orders.user_id = users.user_id WHERE `status` = %s''',
                (status,)
            )
            return cur.fetchall()


    def save(self) -> None:
        self.con.commit()


    def close(self) -> None:
        self.con.close()
