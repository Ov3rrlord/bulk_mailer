#!/bin/python3

import ssl
from smtplib import SMTPAuthenticationError
from smtplib import SMTP_SSL
import threading

# ? import maskpass as mk

password = ""  # new change
receiver = []  # new change
mails = ""


def main():
    smtp_server = "smtp.gmail.com"
    port = 465
    print("***********************************")
    print("* Welcome to the bulk mail sender *")
    print("***********************************\n")
    sender = ""  # insert your gmail address here
    

    def pwd():
        global password
        #  you need to provide a file that contain your password.
        # The file needs to be in th same directory. Or you must specify its path
        try:
            with open("pass.txt", encoding="utf-8") as f:
                for line in f:
                    password = line.strip()
            return password
        except FileNotFoundError:
            print("You need to provide a file containing your google account app password as pass.txt")

    def bulk():
        global receiver
        # ? here you need to provide the file containing the mails you want to send messages to.
        try:
            with open("mails.txt", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    receiver.append(line.strip())
                return receiver
        except FileNotFoundError:
            print("You need to provide a file containing a list of mails as mails.txt")

    def rest():
        global password, mails  # new change
        # receiver = input("Print the receiver email here: ")
        subject = input("Please enter the subject: ")
        content = input("Enter your message here: ")
        context = ssl.create_default_context()
        mails = bulk()

        # connect to the smtp server
        with SMTP_SSL(smtp_server, port, context=context) as server:
            # use try and except to handle exceptions
            try:
                # ask for the password but masked you can use this command instead if you want to type the
                # password via your terminal without the file ù
                # pwd = mk.advpass("Enter your password: ")

                server.login(sender, pwd())  # new change
                print(f"Connected successfully to the SMTP server! {chr(0x1F63A)}\n")

                for mail in mails:  # new change
                    message = f"From: {sender}\nTo: {mail}\nSubject: {subject}\n\n" + str(content)  # new change
                    print("Sending mail to:", mail)  # new change
                    server.sendmail(sender, mail, message)# new change
                    print("="*50)

                print(f"Message sent successfully to {receiver} {chr(0x1F60E)}\n")
            except SMTPAuthenticationError as e:
                print("="*50)
                print(f"Authentication failed {chr(0x1F62B)}. Check the error message bellow to see whats "
                      f"going on: \n" + str(e))
                print("="*50)
            except Exception as e:
                print("="*50)
                print(f"Something went wrong {chr(0x1F914)}. Check the error message bellow to see whats "
                      f"going on:\n" + str(e))
                print("="*50)

            finally:
                server.quit()
                print("Now the server is closed!")
                print("="*50)
                print("Thank you for using the bulk mail sender")
                print("="*50)
                
    rest()



x = threading.Thread(target=main)
x.start()
x.join()
