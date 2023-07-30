#!/bin/python3

from smtplib import SMTP_SSL
from smtplib import SMTPAuthenticationError
import ssl

# import maskpass as mk

password = ""  # new change
receiver = []  # new change
mails = ""


def main():
    smtp_server = "smtp.gmail.com"
    port = 465
    print("Welcome to the bulk mail sender")
    print("********************************")
    sender = "oversecdev@gmail.com"
    subject = input("Please enter the subject:")

    def pwd():
        global password
        with open("pass.txt", encoding="utf-8") as f:
            for line in f:
                password = line.strip()
        return password

    def bulk():
        global receiver
        with open("mails.txt", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                receiver.append(line.strip())
            return receiver

    def rest():
        global password, mails  # new change
        # receiver = input("Print the receiver email here: ")
        content = input("Enter your message here: ")
        context = ssl.create_default_context()
        mails = bulk()

        # connect to the smtp server
        with SMTP_SSL(smtp_server, port, context=context) as server:
            # use try and except to handle exceptions
            try:
                # ask for the password but masked
                # pwd = mk.advpass("Enter your password: ")

                server.login(sender, pwd())  # new change
                print("Server connected successfully \n")

                for mail in mails:  # new change
                    message = f"From: {sender}\nTo: {mail}\n{subject}\n\n" + str(content)  # new change
                    print("Sending mail to:",mail) # new change
                    server.sendmail(sender, mail, message)  # new change
                print("Message sent successfully! \n")
            except SMTPAuthenticationError as e:
                print("Authentication failed: \n" + str(e))
            except Exception as e:
                print("Something went wrong ;/ \n" + str(e))
            finally:
                server.quit()
                print("Server closed")

    rest()


main()
