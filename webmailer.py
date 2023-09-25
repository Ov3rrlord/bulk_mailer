import streamlit as st
import smtplib
import ssl

smtp_server = "smtp.gmail.com"
port = 465

def main():
    with st.form("Bulk mailer"):

        st.date_input("Date")
        name = st.text_input("The From name",placeholder="from name")
        sender = st.text_input("Your gmail address", placeholder="email")
        password = st.text_input("Your gmail password", placeholder="password", type="password")
        receiver = st.text_input("Rceiver", placeholder='receiver mail', help="You can input any email address here")
        st.file_uploader("upload the list of mails")
        subject = st.text_input("Enter the subject", placeholder="Subject")
        content= st.text_area("message")   
        message = f"From: {name}<{sender}>\nTo: {receiver}\nSubject: {subject}\n\n{content}"
        submit = st.form_submit_button("Submit")

        def connection(sender, password):
            password = password
            sender = sender
            context = ssl.create_default_context()
            if submit:
                with st.spinner("Please wait"):

                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        try:
                            server.login(sender, password)
                            st.success("Logged in successfully")
                            server.sendmail(sender, receiver, message)
                        except smtplib.SMTPAuthenticationError:
                            st.warning("Something went wrong while trying logging in")
                        finally:
                            server.quit()
        connection(sender, password)
main()