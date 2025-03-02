import sqlite3
import os


class UsersTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'users'
    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                chat_id int,
                lang text,
                access date,
                reffer_by int,
                status varchar
                )
                    """)

        self.con.commit()
        self.con.close()



    async def delete(self,  chat_id):
        self.cur.execute(f"""
         delete from {self.name} where chat_id=?
        """, (str(chat_id), ))
        self.con.commit()
        self.con.close()

    async def update_status(self, chat_id, status):
        try:
            self.cur.execute(
                f"""
                UPDATE {self.name} SET status=? WHERE chat_id=?
                """, (status, chat_id)
            )
            self.con.commit()
            if self.cur.rowcount > 0:
                updated_data = self.cur.execute(
                    f"""
                    SELECT * FROM {self.name} WHERE chat_id=?
                    """, (chat_id,)
                ).fetchone()
                return updated_data
            else:
                return None
        finally:
            self.con.close()

    async def adduser(self, chat_id, lang=None, access=None, reffer_by=None, status=None):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(?, ?, ?, ?,?)
            """, (
                chat_id,
                lang,
                access,
                reffer_by,
                status
                )
            )

            self.con.commit()
            self.con.close()

        elif lang:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  lang=? where chat_id=?  
                """, (lang, chat_id))
            self.con.commit()
            self.con.close()
        elif access:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  access=? where chat_id=?  
                """, (access, chat_id))
            self.con.commit()
            self.con.close()

    async def search_status(self, chat_id=None):
        if chat_id:
            # So'rovni bajarish
            self.cur.execute(
                f"""
                   SELECT * FROM {self.name} WHERE chat_id=?
               """, (chat_id,)
            )
            response = self.cur.fetchone()
            if response:
                columns = [col[0] for col in self.cur.description]
                result = dict(zip(columns, response))
                return result
            return None
    async def search(self, chat_id=None, all=None, reffer_by=None):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id='{chat_id}'
            """).fetchall()
            if response:
                return response[0]
            return False

        elif reffer_by:
            response = self.cur.execute(
                f"""
                       select count(*) from {self.name} where reffer_by={reffer_by}
                   """).fetchone()
            return response
        else:
            return None

class ExtraTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'extrausers'
    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                chat_id int,
                name text,
                last_usage date,
                usage_count int
                )
                    """)

        self.con.commit()
        self.con.close()



    async def delete(self,  chat_id):
        self.cur.execute(f"""
         delete from {self.name} where chat_id=?
        """, (str(chat_id), ))
        self.con.commit()
        self.con.close()

    async def adduser(self, chat_id, name=None, last_usage=None, usage_count=None):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    ?, ?, ?, ?
                )
            """, (
                chat_id,
                name,
                last_usage,
                usage_count
                )
            )

            self.con.commit()
            self.con.close()

        elif last_usage:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  last_usage=? where chat_id=?  
                """, (last_usage, chat_id))
            self.con.commit()
            self.con.close()
        elif usage_count:
            self.cur.execute(
                f"""
                    update  {self.name}
                    set  usage_count=? where chat_id=?  
                """, (usage_count, chat_id))
            self.con.commit()
            self.con.close()

    async def search(self, chat_id=None, all=None):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id='{chat_id}'
            """).fetchall()
            if response:
                return response[0]
            return False
        return None

class TariffsTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'tariffs'

    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                title text,
                days text,
                price text
                )
                    """)

        self.con.commit()
        self.con.close()
    async def delete(self,  days):
        self.cur.execute(f"""
        delete from {self.name} where days={days}
        """)
        self.con.commit()
        self.con.close()

    async def add(self, title, days, price):
        if not await self.search(days):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    '{title}','{days}', '{price}'
                )
            """)
            self.con.commit()
            self.con.close()
    async def search(self, days=None, title=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif title:
            response = self.cur.execute(
                f"""
                select * from {self.name} where title='{title}'
            """).fetchall()
            if response:
                return response[0]
            return False
        elif days:
            response = self.cur.execute(
                f"""
                select * from {self.name} where days={days}
            """).fetchall()
            if response:
                return response[0]
            return False
        return []

class TokensTable:
    def __init__(self, name="database"):
        self.con = sqlite3.connect(f'{name}.db')
        self.cur = self.con.cursor()
        self.name = 'tokens'

    async def create(self):
        self.cur.execute(
            f"""
                   create table if not exists {self.name} (
                   token text,
                   days text
                   )
                       """)
        self.con.commit()
        self.con.close()
    async def delete(self,  token):
        self.cur.execute(f"""
        delete from {self.name} where token='{token}'
        """)
        self.con.commit()
        self.con.close()

    async def search(self, token=None, days=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif token:
            response = self.cur.execute(
                f"""
                select * from {self.name} where token='{token}'
            """).fetchall()
            if response:
                return response[0]
            return False
        elif days:
            response = self.cur.execute(
                f"""
                select * from {self.name} where days='{days}'
            """).fetchall()

            return response
        return []
    async def add(self, token, days):
        if not await self.search(token=token):
            self.cur.execute(
                f"""
                insert into tokens values(
                    '{token}','{days}'
                )
            """)

            self.con.commit()
            self.con.close()


class ChannelsTable:
    def __init__(self, name="channels"):
        self.name = name
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.users = 'users'

    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                chat_id text
                )
                    """)

        self.con.commit()
        self.con.close()
    async def addchannel(self, chat_id):
        if not await self.search(chat_id=chat_id):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    '{chat_id}'
                )
            """)

            self.con.commit()
            self.con.close()
    async def search(self, chat_id=None, all=False):
        if all:
            response = self.cur.execute(
                f"""
                       select * from {self.name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {self.name} where chat_id={chat_id}
            """).fetchall()
            if response:
                return response[0]
            return False
        else:
            return None

    async def delete(self, chat_id):
        self.cur.execute(f"""
        delete from {self.name} where chat_id='{chat_id}'
        """)
        self.con.commit()
        self.con.close()


class LessonsTable:
    def __init__(self, name="lessons"):
        self.name = name
        self.con = sqlite3.connect('database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    async def create(self):
        self.cur.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.name} (
                    created_at DATE,
                    created_by TEXT,
                    group_id TEXT,
                    name TEXT,
                    message_id INTEGER PRIMARY KEY
                )
            """
        )
        self.con.commit()

    async def add(self, created_at, created_by, group_id, name, message_id):
        if not await self.search(message_id=message_id):
            self.cur.execute(
                f"""
                INSERT INTO {self.name} (created_at, created_by, group_id, name, message_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (created_at, created_by, group_id, name, message_id)
            )
            self.con.commit()

    async def search(self, name=None, message_id=None):
        if message_id:
            response = self.cur.execute(
                f"""
                SELECT * FROM {self.name} WHERE message_id = ?
                """,
                (message_id,)
            ).fetchone()
            return response
        elif name:
            response = self.cur.execute(
                f"""
                SELECT * FROM {self.name} WHERE name = ?
                """,
                (name,)
            ).fetchall()
            return response
        else:
            response = self.cur.execute(
                f"""
                SELECT * FROM {self.name}
                """
            ).fetchall()
            return response

    async def delete(self, message_id):
        self.cur.execute(
            f"""
            DELETE FROM {self.name} WHERE message_id = ?
            """,
            (message_id,)
        )
        self.con.commit()

    def close(self):
        self.con.close()





class SignalsTable:
    def __init__(self, name="signals"):
        self.name = name
        self.con = sqlite3.connect('database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    async def create(self):
        # Jadvalni yaratish
        self.cur.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at DATE,
                    created_by INTEGER,
                    signal_name TEXT,
                    signal_type_id INTEGER,
                    status TEXT
                )
            """
        )
        self.con.commit()

    async def add(self, created_by, signal_name, signal_type_id, status):
        print(created_by, signal_name, signal_type_id, status)
        try:
            self.cur.execute(
                f"""
                INSERT INTO {self.name} (created_by, signal_name, signal_type_id, status)
                VALUES (?, ?, ?, ?)
                """,
                (created_by, signal_name, signal_type_id, status)
            )
            self.con.commit()

            # INSERT ishlaganligini tekshirish
            if self.cur.rowcount > 0:
                print("INSERT muvaffaqiyatli bajarildi")
                return True
            else:
                print("INSERT bajarilmadi")
                return False
        except Exception as e:
            print(f"Xatolik: {e}")
            return False

    async def search_by_status(self, status=None):
        if status:
            # So'rovni bajarish
            self.cur.execute(
                f"""
                SELECT * FROM {self.name} WHERE status = ?
                """,
                (status,)
            )
            response = self.cur.fetchall()  # Barcha natijalarni olish
            if response:
                # Ustun nomlarini olish
                columns = [column[0] for column in self.cur.description]
                # Har bir qatorni dict qilib shakllantirish
                result = [dict(zip(columns, row)) for row in response]
                return result
        return []

    async def delete(self, signal_type_id):
        # signal_type_id bo'yicha o'chirish
        self.cur.execute(
            f"""
            DELETE FROM {self.name} WHERE signal_type_id = ?
            """,
            (signal_type_id,)
        )
        self.con.commit()

    def close(self):
        # Bazani yopish
        self.con.close()


class BarchartTokenTable:
    def __init__(self, name="barchart"):
        self.name = name
        self.con = sqlite3.connect('database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    async def create(self):
        # Jadvalni yaratish
        self.cur.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT DEFAULT (CURRENT_TIMESTAMP),
                    created_by INTEGER,
                    cookie TEXT,
                    cookie2 TEXT,
                    cookie3 TEXT,
                    token TEXT,
                    status TEXT DEFAULT 'ACTIVE'
                )
            """
        )
        self.con.commit()

    async def add_token(self, created_by, token,status):
        print(created_by, token)
        try:
            self.cur.execute(
                f"""
                INSERT INTO {self.name} (created_by, token,status)
                VALUES (?, ?, ?)
                """,
                (created_by, token, status)
            )
            self.con.commit()

            # INSERT ishlaganligini tekshirish
            if self.cur.rowcount > 0:
                print("INSERT muvaffaqiyatli bajarildi")
                return True
            else:
                print("INSERT bajarilmadi")
                return False
        except Exception as e:
            print(f"Xatolik: {e}")
            return False

    async def search_by_status(self, status=None):
        if status:
            # So'rovni bajarish
            self.cur.execute(
                f"""
                SELECT * FROM {self.name} WHERE status = ?
                order by created_at DESC limit 1
                """,
                (status,)
            )
            response = self.cur.fetchone()  # Barcha natijalarni olish
            if response:
                # Ustun nomlarini olish
                columns = [column[0] for column in self.cur.description]
                # Natijani dict shaklida qaytarish
                return dict(zip(columns, response))

        return []

    async def update_cookie1(self, cookie):
        try:
            self.cur.execute(
                f"""
                UPDATE {self.name}
                SET cookie = ?
                WHERE id = (SELECT MAX(id) FROM {self.name})
                """, (cookie,)  # ✅ Tuple sifatida berish kerak
            )
            self.con.commit()
        finally:
            self.con.close()
    async def update_cookie2(self, cookie2):
        try:
            self.cur.execute(
                f"""
                UPDATE {self.name}
                SET cookie2 = ?
                WHERE id = (SELECT MAX(id) FROM {self.name})
                """, (cookie2,)  # ✅ Tuple sifatida berish kerak
            )
            self.con.commit()
        finally:
            self.con.close()
    async def update_cookie3(self, cookie3):
        try:
            self.cur.execute(
                f"""
                UPDATE {self.name}
                SET cookie3 = ?
                WHERE id = (SELECT MAX(id) FROM {self.name})
                """, (cookie3,)  # ✅ Tuple sifatida berish kerak
            )
            self.con.commit()
        finally:
            self.con.close()
    async def delete(self, status):
        # signal_type_id bo'yicha o'chirish
        self.cur.execute(
            f"""
            DELETE FROM {self.name} WHERE status = ?
            """,
            (status,)
        )
        self.con.commit()

    def close(self):
        # Bazani yopish
        self.con.close()


async def setup_tables():
    await UsersTable().create()
    await ExtraTable().create()
    await TariffsTable().create()
    await TokensTable().create()
    await ChannelsTable().create()
    await LessonsTable().create()
    await SignalsTable().create()
    await BarchartTokenTable().create()
