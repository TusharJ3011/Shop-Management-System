import smtplib

SERVER_ADDRESS = "idbmsn3group2@yahoo.com"
OWNER_ADDRESS = "20UCS211@lnmiit.ac.in"
SERVER_PASS = "ogisgjfnihiclsoc"


def outOfStockMail(name):
    connection = smtplib.SMTP("smtp.mail.yahoo.com", 587, timeout=120)
    connection.starttls()
    connection.login(user=SERVER_ADDRESS, password=SERVER_PASS)
    msg = f"Dear Owner,\nKindly note that {name} has gone OUT OF STOCK today.\nShop Management System"
    connection.sendmail(from_addr=SERVER_ADDRESS, to_addrs=OWNER_ADDRESS, msg=f"Subject:Product Out Of Stock\n\n{msg}")
    connection.close()

