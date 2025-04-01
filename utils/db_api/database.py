import sqlite3
import os
from loader import BASE_DIR

class DataBaseSql:
    def __init__(self, name="tokens"):
        self.name = name
        self.con = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
        self.cur = self.con.cursor()
        self.users = 'users'

    async def create(self):
        self.cur.execute(
            f"""
                create table if not exists {self.name}(
                token text
                )
                    """)

        self.con.commit()
        self.con.close()
    async def create_users(self):
        self.cur.execute(
            f"""
                create table if not exists {self.users} (
                chat_id text,
                name text,
                access text
                
                )
                    """)

        self.con.commit()
        self.con.close()
    async def create_tariff(self):
        self.cur.execute(
            f"""
                create table if not exists tariff(
                title text,
                days text,
                price text
                )
                    """)

        self.con.commit()
        self.con.close()

    async def clear(self):
        self.cur.execute(
            f"""
                delete from {self.name}
            """)

        self.con.commit()
        self.con.close()

    async def delete(self,  token):
        self.cur.execute(f"""
        delete from {self.name} where token='{token}'
        """)
        self.con.commit()
        self.con.close()


    async def addtoken(self, token):
        if not await self.search(token=token):
            self.cur.execute(
                f"""
                insert into {self.name} values(
                    '{token}'
                )
            """)

            self.con.commit()
            self.con.close()

    async def adduser(self, chat_id, name=None, access=None):
        if not await self.search_user(chat_id=chat_id):
            self.cur.execute(
                f"""
                            insert into users values(
                            ?, ?, ?
                            )
                        """, (chat_id, name, access))
            self.con.commit()
            self.con.close()
        elif access:
            self.cur.execute(
                f"""
                                        update  users
                                            set  access=? where chat_id=?  
                                    """, (access, chat_id))
            self.con.commit()
            self.con.close()
        else:
            self.cur.execute(
                f"""
                            update  users
                                set name=?, access=? where chat_id=?  
                        """, (name, access, chat_id))
            self.con.commit()
            self.con.close()

    async def delete_user(self,  chat_id):
        self.cur.execute(f"""
            delete from users where chat_id=?  
        """, (chat_id,))
        self.con.commit()
        self.con.close()
    async def search(self, token=None, all=False):
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
        else:
            return None
    async def search_user(self, chat_id=None, all=False):
        name = 'users'
        if all:
            response = self.cur.execute(
                f"""
                       select * from {name}
                   """).fetchall()
            return response
        elif chat_id:
            response = self.cur.execute(
                f"""
                select * from {name} where chat_id={chat_id}
            """).fetchall()
            if response:
                return response[0]
            return False
        else:
            return None

    async def drop(self):
        await self.cur.execute(f'''
                                    DROP TABLE {self.name}
                            ''')
        print(f"Drop {self.name} table")

    async def close(self):
        print("not found close")