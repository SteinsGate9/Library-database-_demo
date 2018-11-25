#!/usr/bin/python
import wx
from SQL import *

def GetCon(name,password):
    conn = None
    global flag
    if(name == 'Admin' and password == '123456'):
        conn = DBadmin()
        if conn == None:
            print("Cannot find user\n")
        else:
            flag = 0
            print("Connected\n")
    else:
        try:
            conn = DBuser(name,password)
        except:
            print("Cannot find user\n")
        else :
            flag = 1
            print("Connected\n")
    return conn

def LogIn():
    Con = None;
    while(input('''Welcome to the lib,\n---Input y if you want to log in.\n---Input n if you want to quit.\n''') != 'n'):
         name = input('''Please Log In:
            Name:''')
         password = input('''
            Password:''')
         Con = GetCon(name,password)
         if(Con != None):
            print("Log in succeeded\n")
            return Con
         else:
            print("Log in failed\n")
    return None


def GetInstructions(user):
    global flag
    op = '1'
    while(op != '10' and op != '7'and user):
        if(flag == 0):
            op = input('''        As admin you can conduct all the following instructions by printing the index:
        ---1.Insert a number of books
        ---2.Update a book that you chooce 
        ---3.Delete a book that you chooce
        ---4.Create a borrowcard
        ---5.Show all the books 
        ---6.Show all the viewers
        ---7.Show all the borrowcards
        ---8.Log in with new id
        ---9.Delete an id
        ---10.EXIT\n''')
            while(op != '10'):
                if(op == '1'):
                    while True:
                        op2 = input("        Please input the name,author,remnant,content(selective),input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            list = op2.split(',')
                            if(len(list) > 4 or len(list) < 3):
                                print("Invalid input\n")
                            else:
                                try:
                                    temBook = Book(list[0], list[1], list[2], list[3])
                                    user.insertBookAsRoot(temBook)
                                except:
                                    print("Insert Failed\n")
                                    user.getAllBook()
                                else:
                                    print("Insert Succeed\n")
                                    user.getAllBook()

                elif(op == '2'):
                    while(True):
                        user.getAllBook()
                        op2 = input("        Please input the name of the book you want to update,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            op3 = input("        Input the name,author,remnant,content\n")
                            list = op3.split(',')
                            if(len(list) != 4):
                                print("Invalid input\n")
                            else:
                                tem = Book(list[0],list[1],list[2],list[3])
                                try:
                                    user.updateBookAsRoot(op2,tem)
                                except:
                                    print("Update failed, probably because you change the name to a existed name\n")
                                else:
                                    print("Update succeeded\n")


                elif(op == '3'):
                    while True:
                        user.getAllBook()
                        op2 = input("        Please input the name you want to delete,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            try:
                                user.deleteBookAsRoot(op2)
                            except:
                                print("Delete failed\n")
                            else:
                                print("Delete succeeded\n")


                elif(op == '4'):
                    while True:
                        op2 = input("        Please input your name,ssn,gender,password; you'll be logging in with your name and password,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            list = op2.split(',')
                            if (len(list) > 4):
                                print("Invalid input\n")
                            else:
                                try:
                                    user.createUserAsRoot(list[0],list[1],list[2],list[3])
                                except:
                                    print("Create User Failed\n")
                                else:
                                    print("Create User Succeeded\n")
                elif(op == '5'):
                     user.getAllBook()

                elif(op == '6'):
                     user.getAllViewer()

                elif(op == '7'):
                     user.getAllBorrowCard()

                elif(op == '8'):
                    Con = LogIn()
                    user = Con
                    break
                elif(op == '9'):
                    while True:
                        user.getAllBorrowCard()
                        op2 = input(
                            "        Please input the name you want to delete,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            try:
                                user.deleteBorrowCardAsRoot(op2)
                            except:
                                print("The id has book not returned\n")
                            else:
                                print("Delete succeeded\n")


                if(op != '8' and op !='10'):
                    op = input('''        As admin you can conduct all the following instructions by printing the index:
        ---1.Insert a number of books
        ---2.Update a book that you chooce 
        ---3.Delete a book that you chooce
        ---4.Create a borrowcard
        ---5.Show all the books 
        ---6.Show all the viewers
        ---7.Show all the borrowcards
        ---8.Log in with new id
        ---9.Delete an id
        ---10.EXIT\n''')

        if(flag == 1):
            op = input('''        As %s you can conduct all the following instructions by printing the index:
        ---1.Borrow a book
        ---2.Return a book
        ---3.Show all the books 
        ---4.Show all the viewers
        ---5.Log in with new id
        ---6.Find a book
        ---7.EXIT1\n'''%user.userName)
            while (op != '7') :
                if op == '1':
                    while True:
                        user.getAllBook()
                        op2 = input(
                            "        Please input the name you want to borrow,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            user.borrowBookAsUser(op2)
                elif op == '2':
                    while True:
                        user.getAllViewer()
                        op2 = input(
                            "        Please input the name you want to return,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            user.returnBookAsUser(op2)
                elif (op == '3'):
                     user.getAllBook()

                elif (op == '4'):
                     user.getAllViewer()

                elif (op == '5'):
                    Con = LogIn()
                    user = Con
                    break
                elif (op == '6'):
                    while True:
                        op2 = input(
                            "        Please input the name you want to find,input n to quit\n")
                        if op2 == 'n':
                            break
                        else:
                            user.getBookByName(op2)


                if(op != '5' and op != '7'):
                    op = input('''        As %s you can conduct all the following instructions by printing the index:
        ---1.Borrow a book
        ---2.Return a book
        ---3.Show all the books 
        ---4.Show all the viewers
        ---5.Log in with new id
        ---6,Find a book
        ---7.EXIT2\n'''%user.userName)



if __name__ == "__main__":
    global flag
    flag = 0
    ThisUser = LogIn()
    if(ThisUser):
        GetInstructions(ThisUser)
    print("GoodBye")
