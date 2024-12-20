import csv
import os
import pandas as pd
import numpy as np
import random
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(match: str, receiver_email: str, address: str):
    load_dotenv()
    # Sender and recipient
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("PASSCODE")

    # Email content
    subject = "2025 Portal Santa Match"
    body = f"""Hello Brother, \n\nYou have {match} for portal santa. There address is {address} \n\n- Eric "The Fiji Santa"
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


def create_derangement(lst):
    """
    Create a random derangement of a list (no element matches its original position).
    """
    while True:
        shuffled = lst[:]
        np.random.shuffle(shuffled)
        if all(original != shuffled[i] for i, original in enumerate(lst)):
            return shuffled


def create_matches() -> pd.DataFrame:
    # Step 1: Read the CSV
    # Replace with your CSV file path
    file_path = "Grad Portal Santa - 2024 Grad Portal Santa.csv"
    df = pd.read_csv(file_path)
    df = df.drop(index=0).reset_index(drop=True)
    df["Match"] = create_derangement(df["Name"].tolist())

    # Display the resulting DataFrame
    print(df)

    result = input("Does this look ok to send the emails(y/n)?")
    if result == 'y':
        for row in df:
            if "Preferred E-mail" in row and "Matches" in row and "Address" in row:
                email = row["Preferred E-mail"]
                match_name = row["Matches"]
                address = row["Address"]

                send_email(match_name, email, address)
            else:
                print(f"-----INVALID ROW ERROR---- {row} ")
    else:
        print("I have failed...")


create_matches()
