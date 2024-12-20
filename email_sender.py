import csv
import smtplib
import os

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(match: str, receiver_email: str):
    load_dotenv()
    # Sender and recipient
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("PASSCODE")

    # Email content
    subject = "2025 Portal Santa Match"
    body = f"""Hello Brother, \n\nYou have {match} for portal santa. \n\n- Eric "The Fiji Santa"
    """

    # Create MIME message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the Gmail SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


file_path = "Portal Santa Matcher - 2024 Matches.csv"

with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    # each row is an ordered dict
    for row in csv_reader:
        if "Preferred E-mail" in row and "Matches" in row:
            email = row["Preferred E-mail"]
            match_name = row["Matches"]
            send_email(match_name, email)
        else:
            print(f"-----INVALID ROW ERROR---- {row} ")
