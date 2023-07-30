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
    print("***********************************")
    print("* Welcome to the bulk mail sender *")
    print("***********************************")
    sender = "oversecdev@gmail.com"  # insert your mail here
    subject = input("Please enter the subject:")

    def pwd():
        global password
        # you need to provide a file that contain your password. 
        # The file needs to be in th same directory. Or you must specify its path
        with open("pass.txt", encoding="utf-8") as f:
            for line in f:
                password = line.strip()
        return password

    def bulk():
        global receiver
        # here you need to provide the file containing the mails you want to send messages to.
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
                # you can use this command instead if you 
                # want to type the password via your terminal without the file
                # pwd = mk.advpass("Enter your password: ")

                server.login(sender, pwd())  # new change
                print("Connected successfully to the SMTP server! 🙂\n")

                for mail in mails:  # new change
                    message = f"From: {sender}\nTo: {mail}\n{subject}\n\n" + str(content)  # new change
                    print("Sending mail to:", mail)  # new change
                    server.sendmail(sender, mail, message)  # new change
                print(f"Message sent successfully to {receiver} 🙂\n")
            except SMTPAuthenticationError as e:
                print("Authentication failed 🙁. Check the error message bellow to see whats going on: \n" + str(e))
            except Exception as e:
                print("Something went wrong 🙁. Check the error message bellow to see whats going on:\n" + str(e))
            except KeyboardInterrupt:
                answer = input("Do you really want to exit ? yes/no").lower()
                if answer == "yes":
                    exit()
                elif answer == "no":
                    main()
            finally:
                server.quit()
                print("Now the server is closed!")

    rest()


main()
