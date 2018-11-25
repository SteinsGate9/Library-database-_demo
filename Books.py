#books
from datetime import *                                               #导入日期模块
__metaclass__ = type
class Book:
    '''一个书本信息类，包括书本名字，作者名字和书本简单信息'''
    def __init__(self, name , author , remnant ,content = ""):
        self.bookName = name                                      #书本名字
        self.bookAuthor = author                                          #作者名字
        self.bookContent = content                                        #书本信息
        self.bookAddDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')                                 #书本添加日期
        self.bookRemnant = remnant

    def setName(self, name):
        self.bookName = name

    def getName(self):
        return self.bookName

    def setAuthor(self, author):
        self.bookAuthor = author

    def getAuthor(self):
        return self.bookAuthor

    def setContent(self, content):
        self.bookContent = content

    def getContent(self):
        return self.bookContent

    def getAddDate(self):
        return self.bookAddDate

    def setRemnant(self, remnant):
        self.bookRemnant = remnant

    def getRemnant(self):
        return self.bookRemnant


if __name__ == "__main__":
    book = Book("crazy","my","content","123")
    print(book.getRemnant(), book.getName())
    # print(mybook.bookName,mybook.bookAuthor,mybook.bookContent,mybook.bookAddDate,mybook.bookRemnant)
    # print(mybook1.bookName, mybook1.bookAuthor, mybook1.bookContent, mybook1.bookAddDate, mybook1.bookRemnant)
    # print(mybook2.bookName, mybook2.bookAuthor, mybook2.bookContent, mybook2.bookAddDate, mybook2.bookRemnant)