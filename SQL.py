import pymysql
from Books import *
from datetime import *

__metaclass__ = type


#
# ok登陆管理员用户
# ok批量入库图书并且查看结果
# ok单次入库一本书，书名等信息由助教当场指定，并查看结果
# ok对刚才入库的单本书进行修改，并查看结果
# 创建一个新的借书证
# 使用刚创建的借书证登陆
# ok查询图书
# 借阅一本书，并且观察图书存量是否正确减少
# 选择一本存量是0的数，演示如果图书存量是0是否能正确提示
# 归还所借的数，并且观察图书存量是否能正确增加
# 查看借书记录，是否能正确显示刚才所借书的借阅日期和归还日子
# 重新借阅一本书，此时切换到管理员用户，试图删除刚才的借书证，是否能正确提示该借书证仍有未归还的书
class DBuser:
    def __init__(self,name,password):
        self.userAdmin = DBadmin()
        self.userName = name
        self.userPassword = password
        self.conn = pymysql.connect(host = "localhost", port = 3306, user = self.userName, password = self.userPassword, db = "library", charset = "utf8")

    def __delete(self):
        self.conn.close();
    def getBookByName(self, name):
        '''根据书本id值来寻找书本信息'''
        sql = "select bookName, bookAuthor, bookContent from book  where bookName = %s"
        conn = self.conn
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))    #参数以元组形式给出
        row = cursor.fetchone()
        if row:
            for items in row:#取到第一个结果
                print(items)
        else:
            print('Book not found\n')
        conn.commit()
        cursor.close()

    def getAllBook(self):
        '''返回数据库中，book表中所有的书本信息'''
        sql = "select *from book;"
        conn = self.conn
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("        All BOOKS LIST:\n")
        for item in rows:
            print(item)
        print("\n")
        conn.commit()
        cursor.close()
        return list

    def borrowBookAsUser(self,name):
        sql = "update  book set bookRemnant = bookRemnant -1 where bookName = %s "
        sql2 = "insert into viewer values(%s,%s,%s,NULL)"
        conn = self.conn
        if conn == None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (name,))
            rownum = conn.commit() # 参数以元组形式给出
        except:
            print("No Remains sorry\n")
            conn.rollback()
            return

        try:
            cursor.execute(sql2, (self.userName,name,datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        except:
            print("Viewer too much")
            conn.rollback()
        cursor.close()
        return

    # and bookName in (select
    # viewerBook
    # from viewer where
    # viewerName = % s and viewerReturnDate is NULL)
    def returnBookAsUser(self,name):
        sql =  "update  book as b set bookRemnant = bookRemnant + 1 where bookName = %s ;"
        sql3 = "select viewerBook from viewer where viewerBook = %s and viewerReturnDate is NULL;"
        sql2 = "update  viewer as b set viewerReturnDate = %s where viewerBook = %s and viewerName = %s and viewerReturnDate is NULL limit 1;"
        conn = self.conn
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql3,name)
        if(not cursor.fetchall()):#not find
            print("You didn't borrow that book\n")
        else:
            try:
                cursor.execute(sql, (name,))
                rownum = conn.commit()  # 参数以元组形式
            except:
                conn.rollback()
            try:
                cursor.execute(sql2, (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), name, self.userName))
                rownum = conn.commit()  # 参数以元组形式
            except:
                conn.rollback()
            else:
                print("Return succeeded\n")


        cursor.close()
        return

    def getAllViewer(self):
        '''返回数据库中，book表中所有的书本信息'''
        sql = "select * from viewer  where viewerName = %s order by viewerBorrowDate"
        conn = self.conn;
        if conn == None:
            return
        cursor = conn.cursor()
        rownum = cursor.execute(sql,self.userName)              #执行并返回找到的行数
        rows = cursor.fetchall()
        list = []
        print("        ALL VIEWERs LIST:\n")
        for item in rows:
            print(item)
        print("\n")
        conn.commit()
        cursor.close()
        return list

    # def getAllBorrowCard(self):
    #     '''返回数据库中，book表中所有的书本信息'''
    #     sql = "select *from viewer"
    #     conn = self.conn;
    #     if conn == None:
    #         return
    #     cursor = conn.cursor()
    #     rownum = cursor.execute(sql)              #执行并返回找到的行数
    #     rows = cursor.fetchall()
    #     list = []
    #     for item in rows:
    #         bitem = (item[0], item[1], item[2],item[3],item[4])
    #         list.append(bitem)
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #     return list






class DBadmin:
    def getLibraryConAsRoot(self):
        '''获取操作数据库的curcor即游标，首先的建立连接，需要服务器地址，端口号，用户名，密码和数据库名'''
        #为了能用中文，得加上编码方式
        conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "123456", db = "library", charset = "utf8")
        return conn

    def createUserAsRoot(self,name,ssn,gender,password):
        sql = "insert into borrowcard(borrowcardName,borrowcardSSN,borrowcardGender,borrowcardAddDate,borrowcardPassword) values(%s, %s, %s, %s,%s);"
        sql2 = "CREATE USER %s@'localhost' IDENTIFIED BY %s; "
        sqlf = "FLUSH PRIVILEGES;"
        sql3 =  "grant select,update(bookRemnant) on book to %s@'localhost'"
        sql4 =  "grant select,update,insert on viewer to  %s@'localhost'"
        conn = self.getLibraryConAsRoot()
        if conn == None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (name, ssn, gender, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), password))  # 插入borrowcard
            conn.commit();
        except:
            print("Already exist")
            conn.rollback();
        else:
            print("Welcome: ", name)
        try:
            cursor.execute(sql2, (name, password))  #创建用户
            conn.commit();
        except:
            conn.rollback();
        try:
            cursor.execute(sqlf)
            conn.commit();
        except:
            conn.rollback();
        try:
            cursor.execute(sql3, (name,))
            conn.commit();
        except:
            conn.rollback();
        try:
            cursor.execute(sql4, (name,))
            conn.commit();
        except:
            conn.rollback();
        cursor.close()
        conn.close()
        new_id = cursor.lastrowid
        user = DBuser(name,password)
        return user

    def insertBooksAsRoot(self,books):
        sql = "insert into book(bookName, bookAuthor, bookContent, bookAddDate,bookRemnant) values(%s, %s, %s, %s,%s)"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        for book in books:
         cursor.execute(sql, (book.getName(), book.getAuthor(), book.getContent(), book.getAddDate(), book.bookRemnant))
        conn.commit()
        cursor.close()
        conn.close()
        return

    def insertBookAsRoot(self, book):
        '''向数据库中book表插入书本信息，book为Book类对象，包含书本基本信息'''
        sql = "insert into book(bookName, bookAuthor, bookContent, bookAddDate,bookRemnant) values(%s, %s, %s, %s,%s)"
        sql2 = "select bookName, bookAuthor, bookContent,bookRemnant from book where bookName = %s and bookAuthor = %s "
        sql3 = "update book set book.bookRemnant =  book.bookRemnant + %s where book.bookName = %s; "
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql2,(book.getName(),book.bookAuthor))
        list = cursor.fetchall()
        if(not list):
            cursor.execute(sql,(book.getName(), book.getAuthor(), book.getContent(), book.getAddDate(), book.bookRemnant))
        else :
            cursor.execute(sql3,(int(book.getRemnant()),book.getName()))
        conn.commit()
        cursor.close()
        conn.close()
        return

    def updateBookAsRoot(self, oldbookname,book):
        '''用book对象来修改id为bookid的书本信息'''
        self.getAllBook()
        sql = "update book set bookName=%s, bookAuthor=%s, bookContent=%s, bookAddDate=%s ,bookRemnant = %s where bookName=%s;"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql, (book.getName(), book.getAuthor(), book.getContent(), datetime.today().strftime('%Y-%m-%d %H:%M:%S'),int(book.bookRemnant),oldbookname))
        conn.commit()
        cursor.close()
        conn.close()

    def checkBorrowWhenDeleteAsRoot(self):
        sql = ''' DELIMITER $
 DROP TRIGGER IF EXISTS bookLimit1$
 CREATE TRIGGER bookLimit1 before update on book
 FOR EACH ROW 
 BEGIN if new.bookRemnant<0 then
 set new.bookRemnant=0;
 #SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT = 'user has been exsits'; 
 end if;
 END$ 
 DELIMITER ;'''
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return

    def getAllBook(self):
        '''返回数据库中，book表中所有的书本信息'''
        sql = "select *from book order by bookAddDate;"
        conn = self.getLibraryConAsRoot()
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("        All BOOKS LIST:\n")
        for item in rows:
            print(item)
        print("\n")
        conn.commit()
        cursor.close()
        return list

    def getAllViewer(self):
        '''返回数据库中，book表中所有的书本信息'''
        sql = "select *from viewer order by viewerBorrowDate"
        conn = self.getLibraryConAsRoot()
        if conn == None:
            return
        cursor = conn.cursor()
        rownum = cursor.execute(sql)              #执行并返回找到的行数
        rows = cursor.fetchall()
        list = []
        print("        ALL VIEWERs LIST:\n")
        for item in rows:
            print(item)
        print("\n")
        conn.commit()
        cursor.close()
        conn.close()
        return list

    def getAllBorrowCard(self):
        '''返回数据库中，book表中所有的书本信息'''
        sql = "select *from borrowcard order by borrowcardAddDate;"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        rownum = cursor.execute(sql)              #执行并返回找到的行数
        rows = cursor.fetchall()
        list = []
        print("        ALL BORROWCARDs LIST:\n")
        for item in rows:
            print(item)
        print("\n")
        conn.commit()
        cursor.close()
        conn.close()
        return list

    def getBookByName(self, name):
        '''根据书本id值来寻找书本信息'''
        sql = "select bookName, bookAuthor, bookContent from book  where bookName = %s"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))                     #参数以元组形式给出
        row = cursor.fetchone()                             #取到第一个结果
        conn.commit()
        cursor.close()
        conn.close()
        return row                                          #返回该书本信息


    def deleteBookAsRoot(self, name):
        '''根据书本id来删除书籍'''
        self.getAllBook()
        sql = "delete from book where bookName = %s"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))
        conn.commit()
        cursor.close()
        conn.close()

    def deleteBorrowCardAsRoot(self, name):
        self.getAllBorrowCard()
        sql = "delete from borrowcard where borrowcardName = %s"
        conn = self.getLibraryConAsRoot();
        if conn == None:
            return
        cursor = conn.cursor()
        cursor.execute(sql, (name,))
        conn.commit()
        cursor.close()
        conn.close()



if __name__ == '__main__':
    db = DBadmin()
    #db.checkBorrowWhenDeleteAsRoot()
    #book = Book("tabook","ta","check")
    users= []
    #db.createUserAsRoot("TA2", "31501038472", "unknown","123456")
   # users .append(user1)
    user2 = DBuser("benson","123456")
    # cursor = user1.conn.cursor()
    # sql2 = "insert into viewer values(%s,%s,%s,NULL)"
    # cursor.execute(sql2, ("TA2", "秦腔", datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

    #user2.returnBookAsUser("秦腔")


