import smtplib
import os

SERVER_ADDRESS = os.environ['SERVER_ADDRESS']
OWNER_ADDRESS = os.environ['OWNER_ADDRESS']
SERVER_PASS = os.environ['SERVER_PASS']


def outOfStockMail(name):
    connection = smtplib.SMTP("smtp.mail.yahoo.com", 587, timeout=120)
    connection.starttls()
    connection.login(user=SERVER_ADDRESS, password=SERVER_PASS)
    msg = f"Dear Owner,\nKindly note that {name} has gone OUT OF STOCK today.\nShop Management System"
    connection.sendmail(from_addr=SERVER_ADDRESS, to_addrs=OWNER_ADDRESS, msg=f"Subject:Product Out Of Stock\n\n{msg}")
    connection.close()
