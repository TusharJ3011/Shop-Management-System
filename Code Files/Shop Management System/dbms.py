from datetime import date, datetime
import mysql.connector

import security
import mail


class AdminProducts:
    def __init__(self):
        self.brands = self.getBrandNames()
        self.products = []
        self.types = []
        self.sBrand = None
        self.sProduct = None
        self.sType = None
        self.price = None
        self.quantity = None
        self.manDate = None
        self.expDate = None
        self.error = False

    def getBrandNames(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute("SELECT brandID, brandName FROM brands ORDER BY brandName DESC")
        brands = myCursor.fetchall()
        brandNames = []
        for brand in brands:
            brandName = f"{brand[1]} ({brand[0]})"
            brandNames.append(brandName)
        return brandNames

    def getBrandProducts(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        brandID = int(self.sBrand[-4:-1])
        brandProducts = []
        myCursor.execute(f"SELECT productID, productName FROM products WHERE brandID={brandID}")
        selectedProducts = myCursor.fetchall()
        for product in selectedProducts:
            string = f'{product[1]} ({product[0]})'
            brandProducts.append(string)
        self.products = brandProducts
        return

    def getProductTypes(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        productID = int(self.sProduct[-4:-1])
        productTypes = []
        myCursor.execute(f"SELECT typeID, typeName FROM types WHERE productID={productID}")
        selectedTypes = myCursor.fetchall()
        for type in selectedTypes:
            string = f'{type[1]} ({type[0]})'
            productTypes.append(string)
        self.types = productTypes
        return

    def isExpired(self, expiry):
        today = date.today()
        isExpiredBool = today >= expiry
        return isExpiredBool

    def restock(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        typeID = int(self.sType[-4:-1])
        myCursor.execute(f"SELECT typeID, productAvailable, typeName, productID FROM types WHERE typeID={typeID}")
        data = myCursor.fetchall()
        data = data[0]
        if data[1] == 0:
            myCursor.execute(
                f"UPDATE types SET manDate='{self.manDate}', expDate='{self.expDate}', productAvailable={self.quantity}, price={self.price} WHERE typeID = {typeID}")
            myDB.commit()
        else:
            self.error = True
            typeName = data[2] + ' - Restock'
            myCursor.execute(
                f"INSERT INTO types(typeName, productID, price, productAvailable, manDate, expDate) VALUES ('{typeName}', {data[3]}, {self.price}, {self.quantity}, '{self.manDate}', '{self.expDate}')")
            myDB.commit()
        return

    def newType(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        productID = int(self.sProduct[-4:-1])
        myCursor.execute(f"SELECT * FROM types WHERE productID={productID} AND typeName='{self.sType}'")
        data = myCursor.fetchall()
        if len(data) == 0:
            myCursor.execute(
                f"INSERT INTO types (typeName, price, productAvailable, manDate, expDate, productID) VALUES('{self.sType}', {self.price}, {self.quantity}, '{self.manDate}', '{self.expDate}', {productID}) ")
            myDB.commit()
        else:
            self.error = True
        return

    def newProduct(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        brandID = int(self.sBrand[-4:-1])
        myCursor.execute(f"SELECT * FROM products WHERE brandID={brandID} AND productName='{self.sProduct}'")
        data = myCursor.fetchall()
        if len(data) == 0:
            myCursor.execute(f"INSERT INTO products (productName, brandID) VALUES('{self.sProduct}', {brandID}) ")
            myDB.commit()
            myCursor.execute(
                f"SELECT productID FROM products WHERE productName='{self.sProduct}' AND brandID={brandID}")
            productID = myCursor.fetchone()
            productID = productID[0]
            myCursor.execute(
                f"INSERT INTO types (typeName, price, productAvailable, manDate, expDate, productID) VALUES('{self.sType}', {self.price}, {self.quantity}, '{self.manDate}', '{self.expDate}', {productID}) ")
            myDB.commit()
        else:
            self.error = True
        return

    def newBrand(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute(f"SELECT * FROM brands WHERE brandName='{self.sBrand}'")
        data = myCursor.fetchall()
        if len(data) == 0:
            myCursor.execute(f"INSERT INTO brands (brandName) VALUES('{self.sBrand}') ")
            myDB.commit()
            myCursor.execute(f"SELECT brandID FROM brands WHERE brandName='{self.sBrand}'")
            brandID = myCursor.fetchone()
            brandID = brandID[0]
            myCursor.execute(f"INSERT INTO products (productName, brandID) VALUES('{self.sProduct}', {brandID}) ")
            myDB.commit()
            myCursor.execute(
                f"SELECT productID FROM products WHERE productName='{self.sProduct}' AND brandID={brandID}")
            productID = myCursor.fetchone()
            productID = productID[0]
            myCursor.execute(
                f"INSERT INTO types (typeName, price, productAvailable, manDate, expDate, productID) VALUES('{self.sType}', {self.price}, {self.quantity}, '{self.manDate}', '{self.expDate}', {productID}) ")
            myDB.commit()
        else:
            self.error = True
        return


class FindProduct:

    def __init__(self):
        self.brands = self.getBrandNames()
        self.products = []
        self.types = []
        self.details = None
        self.sBrand = None
        self.sProduct = None
        self.sType = None
        self.errorCode = 'noerror'

    def getBrandNames(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute("SELECT brandID, brandName FROM brands ORDER BY brandID ASC")
        brands = myCursor.fetchall()
        brandNames = []
        for brand in brands:
            brandName = f"{brand[1]} ({brand[0]})"
            brandNames.append(brandName)
        return brandNames

    def getBrandProducts(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        brandID = int(self.sBrand[-4:-1])
        brandProducts = []
        myCursor.execute(f"SELECT productID, productName FROM products WHERE brandID={brandID}")
        selectedProducts = myCursor.fetchall()
        for product in selectedProducts:
            string = f'{product[1]} ({product[0]})'
            brandProducts.append(string)
        self.products = brandProducts
        return

    def getProductTypes(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        productID = int(self.sProduct[-4:-1])
        productTypes = []
        myCursor.execute(f"SELECT typeID, typeName FROM types WHERE productID={productID}")
        selectedTypes = myCursor.fetchall()
        for type in selectedTypes:
            string = f'{type[1]} ({type[0]})'
            productTypes.append(string)
        self.types = productTypes
        return

    def isExpired(self, expiry):
        today = date.today()
        isExpiredBool = today >= expiry
        return isExpiredBool

    def getDetails(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        typeID = int(self.sType[-4:-1])
        myCursor.execute(f"SELECT * FROM types WHERE typeID={typeID}")
        type = myCursor.fetchall()
        type = type[0]
        type = list(type)
        type.pop()
        if self.isInStock(type) and not self.isExpired(type[4]):
            type.append('available')
        else:
            type.append('not available')
        type = tuple(type)
        self.details = type
        return

    def isInStock(self, details):
        if details[5] > 0:
            return True
        else:
            return False

    def resetAfterftype(self):
        self.details = None
        self.sType = None
        self.types = []
        return

    def resetAfterfpro(self):
        self.sType = None
        self.sProduct = None
        self.details = None
        self.types = []
        self.products = []
        return


class Checkout(FindProduct):

    def __init__(self):
        super().__init__()
        self.cost = 0
        self.amount = None
        self.tags = []
        self.addedProducts = [[], [], []]

    def getPrice(self):
        return self.details[2]

    def getProductID(self):
        return self.sBrand[-4:-1] + self.sProduct[-4:-1] + self.sType[-4:-1]

    def isProductAdded(self, ID, quantity, availableQuantity):
        if ID in self.addedProducts[0]:
            index = self.addedProducts[0].index(ID)
            quantitycan = self.addedProducts[2][index] - self.addedProducts[1][index]
            if quantitycan < quantity:
                self.addedProducts[1][index] = self.addedProducts[2][index]
                value = quantitycan
            else:
                self.addedProducts[1][index] += quantity
                value = quantity
        else:
            self.addedProducts[0].append(ID)
            self.addedProducts[1].append(quantity)
            self.addedProducts[2].append(availableQuantity)
            value = quantity
        return value

    def checkout(self, details):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute(f"INSERT INTO billbook(shopID, empID, dateOfPurchase, totalCost) VALUES {details}")
        myDB.commit()
        myCursor.execute(f"SELECT billID FROM billbook ORDER BY billID DESC LIMIT 1")
        ID = myCursor.fetchone()
        ID = ID[0]
        for PID in self.addedProducts[0]:
            myCursor.execute(f"INSERT INTO productsBought VALUES ({ID}, '{PID}')")
            myDB.commit()
        return

    def getCheckoutAddDetails(self, quantity):
        self.getDetails()
        list = []
        list.append(self.getProductID())
        string = self.sBrand[:-6] + ' ' + self.sProduct[:-6] + ' ' + self.sType[:-6]
        list.append(string)
        list.append(self.details[2])
        if quantity > self.details[5]:
            newQuantity = self.details[5]
        else:
            newQuantity = quantity
        list.append(newQuantity)
        price = newQuantity * self.details[2]
        list.append(price)
        list.append(self.details[5])
        if self.details[6] == 'available':
            list[3] = self.isProductAdded(list[0], list[3], list[5])
            list[4] = list[3] * self.details[2]
            self.tags.append(list)
            self.cost += list[4]
            if quantity > list[3]:
                self.errorCode = 'warning'
            else:
                self.errorCode = 'noerror'
        else:
            self.errorCode = 'danger'
        return

    def decStock(self):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        list = []
        for data in self.addedProducts[0]:
            str = data[-3:]
            str = int(str)
            list.append(str)
        length = len(list)
        for i in range(0, length):
            myCursor.execute(f"SELECT productAvailable FROM types WHERE typeID={list[i]}")
            data = myCursor.fetchone()
            data = int(data[0])
            newStock = data - self.addedProducts[1][i]
            myCursor.execute(f"UPDATE types SET productAvailable={newStock} WHERE typeID={list[i]}")
            if newStock == 0:
                if self.checkRestockAvailibility(list[i]):
                    name = self.findFullName(list[i])
                    mail.outOfStockMail(name)
            myDB.commit()
        return

    def cleanCheckout(self):
        (self.sType, self.sBrand, self.sProduct, self.details) = (None, None, None, None)
        self.products = []
        self.types = []
        return

    def findFullName(self, typeID):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute(f"SELECT typeName, productID FROM types WHERE typeID={typeID}")
        data = myCursor.fetchone()
        typeName = data[0]
        myCursor.execute(f"SELECT productName, brandID FROM products WHERE productID={data[1]}")
        data = myCursor.fetchone()
        productName = data[0]
        myCursor.execute(f"SELECT brandName FROM brands WHERE brandID={data[1]}")
        data = myCursor.fetchone()
        brandName = data[0]
        fullName = f'{brandName} : {productName} : {typeName}'
        return fullName

    def checkRestockAvailibility(self, typeID):
        temp = createRunners()
        myDB = temp[0]
        myCursor = temp[1]
        myCursor.execute(f"SELECT typeName FROM types WHERE typeID={typeID}")
        data = myCursor.fetchone()
        typeName = data[0]
        newTypeName = f"{typeName} - Restock"
        myCursor.execute(f"SELECT * FROM types WHERE typeName='{newTypeName}'")
        data = myCursor.fetchall()
        if len(data) == 0:
            return True
        else:
            data = data[0]
            myCursor.execute(f"UPDATE types SET price={data[2]}, manDate='{data[3]}', expDate='{data[4]}', productAvailable={data[5]} WHERE typeID={typeID}")
            myDB.commit()
            myCursor.execute(f"DELETE FROM types WHERE typeID={data[0]}")
            myDB.commit()
            return False


def createRunners():
    myDB = mysql.connector.connect(
        host="remotemysql.com",
        user="lwJskOUFdk",
        password="mpK8xPst6r",
        database="lwJskOUFdk"
    )
    myCursor = myDB.cursor()
    return [myDB, myCursor]


def getShops():
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    shops = []
    myCursor.execute("SELECT shopID, shopName FROM shops")
    data = myCursor.fetchall()
    for shop in data:
        string = f'{shop[1]} ({shop[0]})'
        shops.append(string)
    return shops


def getEmployees():
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    employees = []
    myCursor.execute("SELECT empID, employeeName FROM employees")
    data = myCursor.fetchall()
    for employee in data:
        string = f'{employee[1]} ({employee[0]})'
        employees.append(string)
    return employees


def getEmployeePassword(employee):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    employeeID = int(employee[-4:-1])
    myCursor.execute(f"SELECT password FROM employees WHERE empID={employeeID}")
    password = myCursor.fetchall()
    password = password[0][0]
    return password


def getTodayRevenue(password):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    if security.checkAdminPassword(password):
        todayDate = date.today().strftime("%Y-%m-%d")
        myCursor.execute(f"SELECT SUM(totalCost) FROM billbook WHERE dateOfPurchase='{todayDate}'")
        cost = myCursor.fetchone()
        cost = str(cost[0])
        result = (cost, False)
    else:
        result = ("-", True)
    return result


def getYearlyRevenue(password, year):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    if security.checkAdminPassword(password):
        myCursor.execute(f"SELECT SUM(totalCost) FROM billbook WHERE YEAR(dateOfPurchase)={year}")
        cost = myCursor.fetchone()
        cost = str(cost[0])
        result = (cost, False)
    else:
        result = ("-", True)
    return result


def getMonthlyRevenue(password, year, month):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    if security.checkAdminPassword(password):
        myCursor.execute(
            f"SELECT SUM(totalCost) FROM billbook WHERE YEAR(dateOfPurchase)={year} AND MONTH (dateOfPurchase)={month}")
        cost = myCursor.fetchone()
        cost = str(cost[0])
        result = (cost, False)
    else:
        result = ("-", True)
    return result


def getDailyRevenue(password, date):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    if security.checkAdminPassword(password):
        date = datetime.strptime(date, '%Y-%m-%d').strftime("%Y-%m-%d")
        myCursor.execute(f"SELECT SUM(totalCost) FROM billbook WHERE dateOfPurchase='{date}'")
        cost = myCursor.fetchone()
        cost = str(cost[0])
        result = (cost, False)
    else:
        result = ("-", True)
    return result


def setNewBranch(details):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    myCursor.execute(f"SELECT shopID FROM shops WHERE shopName='{details[0]}'")
    data = myCursor.fetchall()
    if len(data) == 0:
        error = False
        myCursor.execute(f"INSERT INTO shops(shopName, shopAddress) VALUES ('{details[0]}', '{details[1]}')")
        myDB.commit()
    else:
        error = True
    return error


def setNewEmployee(details):
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    securePass = security.securePassword(details[1])
    dob = datetime.strptime(details[3], '%Y-%m-%d').strftime("%Y-%m-%d")
    myCursor.execute(
        f"INSERT INTO employees(employeeName, password, phoneNumber, dateOfBirth, address) VALUES ('{details[0]}', '{securePass}', {details[2]}, '{dob}', '{details[4]}')")
    myDB.commit()
    return


def getLogs():
    temp = createRunners()
    myDB = temp[0]
    myCursor = temp[1]
    logs = []
    myCursor.execute("SELECT * FROM billbook")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT * FROM brands")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT * FROM products")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT * FROM types")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT * FROM shops")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT empID, employeeName, phoneNumber, dateOfBirth, address FROM employees")
    logs.append(myCursor.fetchall())
    myCursor.execute("SELECT * FROM productsBought")
    logs.append(myCursor.fetchall())
    logs = tuple(logs)
    return logs
