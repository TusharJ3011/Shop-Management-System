import werkzeug.security
import os

ADMINUSERNAME = os.environ['ADMIN_USER'].lower()
ADMINPASSWORD = os.environ['ADMIN_PASS']


def securePassword(password):
    securePass = werkzeug.security.generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=16)
    return securePass


def checkAdmin(username, password):
    error = []
    if username.lower() == ADMINUSERNAME:
        error.append(0)
        passCheck = werkzeug.security.check_password_hash(pwhash=ADMINPASSWORD, password=password)
        if passCheck:
            error.append(0)
        else:
            error.append(1)
    else:
        error.append(1)
        error.append(1)
    return error


def checkAdminPassword(password):
    passCheck = werkzeug.security.check_password_hash(pwhash=ADMINPASSWORD, password=password)
    return passCheck


import dbms


def checkEmployee(employee, password):
    cPassword = dbms.getEmployeePassword(employee)
    if werkzeug.security.check_password_hash(pwhash=cPassword, password=password):
        return True
    else:
        return False
