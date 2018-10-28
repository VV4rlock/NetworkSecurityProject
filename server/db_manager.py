
import pymysql as mysql
import hashlib
import re

class Category_exist_exception(Exception):
    pass

class User_exist_exception(Exception):
    pass

class DbManager:
    def __init__(self):
        hostname = "127.0.0.1"
        user = "vlad"
        passwd = "123"
        dbname = "db_project"
        charset = "utf8"
        self.db = mysql.connect(host=hostname,port=3306, user=user, passwd=passwd, db=dbname, charset=charset)


    def signup(self,login,password):
        login=re.escape(login)
        password=re.escape(password)
        cursor = self.db.cursor()
        cursor.execute("select * from `users` where login='{}'".format(login))
        users=cursor.fetchall()
        if len(users)!=0:
            raise User_exist_exception()
        md5 = hashlib.md5()
        md5.update(password)

        sql = """INSERT INTO `users` (`id`, `login`, `pass`)
         VALUES (NULL, '{}', '{}')""".format(login,md5.hexdigest())
        cursor.execute(sql)
        self.db.commit()
        return True

    def get_account_by_id(self,id):
        #id=re.escape(id)
        cursor = self.db.cursor()
        sql = """SELECT login FROM `users` WHERE id='{}' """.format(id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==1:
            return data[0]
        return None

    def get_sesskey(self,login):
        login=re.escape(login)
        cursor = self.db.cursor()
        sql = """SELECT `sess_key` FROM `sess` WHERE `user`='{}' """.format(login)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            return data[0][0]
        return None

    def set_sesskey(self,login,key):
        login = re.escape(login)
        cursor = self.db.cursor()
        sql = """SELECT `sess_key` FROM `sess` WHERE user='{}' """.format(login)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            sql = """UPDATE `sess` SET 
                            `sess_key`='{}' WHERE user='{}' """.format(key,login)
            cursor.execute(sql)
            self.db.commit()
        else:
            sql = """INSERT INTO `sess` (`id`, `user`, `sess_key`)
                     VALUES (NULL, '{}', '{}')""".format(login, key)
            print(sql)
            cursor.execute(sql)
            self.db.commit()

    def change_pass(self,login,old_pass,new_pass):
        login = re.escape(login)
        old_pass = re.escape(old_pass)
        new_pass = re.escape(new_pass)
        md5=hashlib.md5()
        md5.update(old_pass.encode())
        cursor = self.db.cursor()
        sql = """SELECT id,login FROM `users` 
                        WHERE login='{}' AND pass='{}' """.format(login, md5.hexdigest())
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        if len(data) == 1:
            update="UPDATE `users` SET `pass` = '{}' WHERE `users`.`login` = '{}'".format(new_pass,login)
            cursor.execute(update)
            self.db.commit()
            return True
        else:
            return False

    def auth(self,login,pass_hash,sess_key):
        login = re.escape(login)
        pass_hash = re.escape(pass_hash)

        cursor = self.db.cursor()
        sql = """SELECT id,login,pass FROM `users` 
                WHERE login='{}' """.format(login)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)==1:
            print(data)
            hash = data[0][2]
            md5 = hashlib.md5()
            md5.update(hash.encode() + sess_key)
            if pass_hash == md5.hexdigest():
                return data[0][0], data[0][1]
        return None





if __name__=="__main__":
    db=DbManager()
    print(db.auth("root", "123"))