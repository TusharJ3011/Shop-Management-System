from flask import render_template, url_for, Flask, request, redirect, session
import datetime as dt

# Local Files
import dbms
import security

app = Flask(__name__)
app.secret_key = 'N3G2_SMS'
app.register_error_handler(404, 'pageNotFound')

WORKING_AGE_LIMIT_DAYS = int(14 * 365.25)

# Global variable for FindProduct.html
global fProduct
fProduct = dbms.FindProduct()

# Global variables for Checkout.html
global checkoutProduct
checkoutProduct = dbms.Checkout()

global restock, newType, newProduct, newBrand, todayData, dateData, monthData, yearData, runningAcc
restock = dbms.AdminProducts()
newType = dbms.AdminProducts()
newProduct = dbms.AdminProducts()
newBrand = dbms.AdminProducts()
todayData = ["", False]
dateData = ["", False]
monthData = ["", False]
yearData = ["", False]
runningAcc = None


@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    global runningAcc
    runningAcc = None
    global fProduct
    fProduct = dbms.FindProduct()
    return render_template('Home.html')


@app.route('/findproduct')
@app.route('/findproduct/')
def findProduct():
    global runningAcc
    runningAcc = None
    global fProduct
    return render_template('FindProduct.html', fProduct=fProduct)


@app.route('/fpro', methods=['POST', 'GET'])
def fpro():
    global runningAcc
    runningAcc = None
    data = request.form
    global fProduct
    if data['brand'] == 'none':
        fProduct.errorCode = 'error'
    else:
        fProduct.resetAfterfpro()
        fProduct.sBrand = data['brand']
        fProduct.errorCode = 'noerror'
        fProduct.getBrandProducts()
    return redirect(url_for('findProduct'))


@app.route('/ftype', methods=['POST', 'GET'])
def ftype():
    global runningAcc
    runningAcc = None
    data = request.form
    global fProduct
    if data['product'] == 'none':
        fProduct.errorCode = 'error'
    else:
        fProduct.resetAfterftype()
        fProduct.sProduct = data['product']
        fProduct.errorCode = 'noerror'
        fProduct.getProductTypes()
    return redirect(url_for('findProduct'))


@app.route('/resetfindproducts', methods=['POST', 'GET'])
def resetFindProducts():
    global runningAcc
    runningAcc = None
    global fProduct
    fProduct.errorCode = 'noerror'
    fProduct = dbms.FindProduct()
    return redirect(url_for('findProduct'))


@app.route('/searchfindproducts', methods=['POST', 'GET'])
def searchFindProducts():
    global runningAcc
    runningAcc = None
    data = request.form
    global fProduct
    if data['type'] == 'none':
        fProduct.errorCode = 'error'
    else:
        fProduct.sType = data['type']
        fProduct.errorCode = 'noerror'
        fProduct.getDetails()
    return redirect(url_for('findProduct'))


@app.route('/checkout')
@app.route('/checkout/')
def checkout():
    global runningAcc
    runningAcc = None
    global fProduct
    fProduct = dbms.FindProduct()

    global checkoutProduct
    length = len(checkoutProduct.tags)
    gst = 0
    tax = gst * checkoutProduct.cost
    checkoutProduct.amount = checkoutProduct.cost + tax
    return render_template('Checkout.html', tax=tax, length=length, checkoutProduct=checkoutProduct)


@app.route('/cpro', methods=['POST', 'GET'])
def cpro():
    global runningAcc
    runningAcc = None
    data = request.form
    global checkoutProduct
    if data['brand'] == 'none':
        checkoutProduct.errorCode = 'error'
    else:
        checkoutProduct.resetAfterfpro()
        checkoutProduct.sBrand = data['brand']
        checkoutProduct.errorCode = 'noerror'
        checkoutProduct.getBrandProducts()
    return redirect(url_for('checkout'))


@app.route('/ctype', methods=['POST', 'GET'])
def ctype():
    global runningAcc
    runningAcc = None
    data = request.form
    global checkoutProduct
    if data['product'] == 'none':
        checkoutProduct.errorCode = 'error'
    else:
        checkoutProduct.resetAfterftype()
        checkoutProduct.sProduct = data['product']
        checkoutProduct.errorCode = 'noerror'
        checkoutProduct.getProductTypes()
        print(checkoutProduct.sBrand)
    return redirect(url_for('checkout'))


@app.route('/resetcheckout', methods=['POST', 'GET'])
def resetcheckout():
    global runningAcc
    runningAcc = None
    global checkoutProduct
    checkoutProduct.cleanCheckout()
    return redirect(url_for('checkout'))


@app.route('/addcheckout', methods=['POST', 'GET'])
def addcheckout():
    global runningAcc
    runningAcc = None
    data = request.form
    global checkoutProduct
    if data['type'] == 'none':
        checkoutProduct.errorCode = 'error'
    else:
        checkoutProduct.resetAfterftype()
        checkoutProduct.sType = data['type']
        checkoutProduct.errorCode = 'noerror'
        quantity = int(data['quantity'])
        checkoutProduct.getCheckoutAddDetails(quantity)
    return redirect(url_for('resetcheckout'))


@app.route('/removetag/<int:index>/<id>/<int:quantity>', methods=['POST', 'GET'])
def removetag(index, id, quantity):
    global runningAcc
    runningAcc = None
    global checkoutProduct
    checkoutProduct.cost -= checkoutProduct.tags[index][4]
    checkoutProduct.tags.pop(index)
    tempIndex = checkoutProduct.addedProducts[0].index(id)
    checkoutProduct.addedProducts[1][tempIndex] = checkoutProduct.addedProducts[1][tempIndex] - quantity
    if checkoutProduct.addedProducts[1][tempIndex] == 0:
        checkoutProduct.addedProducts[0].pop(tempIndex)
        checkoutProduct.addedProducts[1].pop(tempIndex)
        checkoutProduct.addedProducts[2].pop(tempIndex)
    return redirect(url_for('checkout'))


@app.route('/proceedcheckout')
def proceedcheckout():
    return redirect(url_for('verifycheckout'))


@app.route('/checkout/verify', methods=['POST', 'GET'])
def verifycheckout():
    global runningAcc
    runningAcc = None
    if request.method == 'POST':
        data = request.form
        shop = data['shop']
        employee = data['employee']
        password = data['password']
        if security.checkEmployee(employee=employee, password=password):
            global checkoutProduct
            date = dt.datetime.today()
            date = date.strftime('%Y-%m-%d')
            list = []
            list.append(int(shop[-4:-1]))
            list.append(int(employee[-4:-1]))
            list.append(date)
            list.append(checkoutProduct.amount)
            bill = tuple(list)
            checkoutProduct.decStock()
            checkoutProduct.checkout(bill)
            checkoutProduct = dbms.Checkout()
            return redirect(url_for('checkout'))
        else:
            shops = dbms.getShops()
            employees = dbms.getEmployees()
            return render_template('checkoutLogin.html', errorCode=True, shops=shops, employees=employees)
    shops = dbms.getShops()
    employees = dbms.getEmployees()
    return render_template('checkoutLogin.html', errorCode=False, shops=shops, employees=employees)


@app.route('/admin')
@app.route('/admin/')
def admin():
    try:
        if session['adminLogin']:
            today = dt.date.today()
            workingYear = today - dt.timedelta(days=WORKING_AGE_LIMIT_DAYS)
            today = today.strftime("%Y-%m-%d")
            workingYear = workingYear.strftime("%Y-%m-%d")
            global restock, newType, newProduct, newBrand, todayData, dateData, monthData, yearData, runningAcc
            return render_template('admin.html', restock=restock, newType=newType, newProduct=newProduct,
                                   newBrand=newBrand, todayData=todayData, dateData=dateData, monthData=monthData,
                                   yearData=yearData, today=today, emindate=workingYear, runningAcc=runningAcc)
        else:
            return redirect(url_for('adminlogin'))
    except (RuntimeError, KeyError):
        return redirect(url_for('adminlogin'))


@app.route('/login', methods=['POST', 'GET'])
@app.route('/login/', methods=['POST', 'GET'])
def adminlogin():
    global runningAcc
    runningAcc = None
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        errorCodes = security.checkAdmin(username=username, password=password)
        if not errorCodes[0] and not errorCodes[1]:
            session['adminLogin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('Login.html', errorCodes=errorCodes)
    errorCodes = [False, False]
    return render_template('Login.html', errorCodes=errorCodes)


@app.route('/admin/logout')
def adminlogout():
    global runningAcc
    runningAcc = None
    session['adminLogin'] = False
    return redirect(url_for('admin'))


@app.route('/logs')
@app.route('/logs/')
def logs():
    logs = dbms.getLogs()
    try:
        if session['adminLogin']:
            return render_template('logs.html', logs=logs)
        else:
            return redirect(url_for('adminlogin'))
    except (RuntimeError, KeyError):
        return redirect(url_for('adminlogin'))


@app.route('/admin/restock/products', methods=['POST', 'GET'])
def restockproduct():
    global restock, runningAcc
    runningAcc = 'restock'
    data = request.form
    restock.sBrand = data['brand']
    restock.getBrandProducts()
    return redirect(url_for('admin'))


@app.route('/admin/restock/types', methods=['POST', 'GET'])
def restocktypes():
    global restock, runningAcc
    runningAcc = 'restock'
    data = request.form
    restock.sProduct = data['product']
    restock.getProductTypes()
    return redirect(url_for('admin'))


@app.route('/admin/restock/add', methods=['POST', 'GET'])
def restockadd():
    global restock, runningAcc
    runningAcc = 'restock'
    data = request.form
    restock.sType = data['type']
    restock.quantity = int(data['quantity'])
    restock.price = int(data['price'])
    restock.manDate = data['mDate']
    restock.expDate = data['eDate']
    restock.restock()
    return redirect(url_for('admin'))


@app.route('/admin/addnt/products', methods=['POST', 'GET'])
def addntproduct():
    global newType, runningAcc
    runningAcc = 'addnt'
    data = request.form
    newType.sBrand = data['brand']
    newType.getBrandProducts()
    return redirect(url_for('admin'))


@app.route('/admin/addnt/add', methods=['POST', 'GET'])
def addntadd():
    global newType, runningAcc
    runningAcc = 'addnt'
    data = request.form
    newType.sProduct = data['product']
    newType.sType = data['type']
    newType.quantity = int(data['quantity'])
    newType.price = int(data['price'])
    newType.manDate = data['mDate']
    newType.expDate = data['eDate']
    newType.newType()
    return redirect(url_for('admin'))


@app.route('/admin/addnp/add', methods=['POST', 'GET'])
def addnpadd():
    global newProduct, runningAcc
    runningAcc = 'addnp'
    data = request.form
    newProduct.sBrand = data['brand']
    newProduct.sProduct = data['product']
    newProduct.sType = data['type']
    newProduct.quantity = int(data['quantity'])
    newProduct.price = int(data['price'])
    newProduct.manDate = data['mDate']
    newProduct.expDate = data['eDate']
    newProduct.newProduct()
    return redirect(url_for('admin'))


@app.route('/admin/addnb/add', methods=['POST', 'GET'])
def addnbadd():
    global newBrand, runningAcc
    runningAcc = 'addnb'
    data = request.form
    newBrand.sBrand = data['brand']
    newBrand.sProduct = data['product']
    newBrand.sType = data['type']
    newBrand.quantity = int(data['quantity'])
    newBrand.price = int(data['price'])
    newBrand.manDate = data['mDate']
    newBrand.expDate = data['eDate']
    newBrand.newBrand()
    return redirect(url_for('admin'))


@app.route('/admin/revenue/today', methods=['POST', 'GET'])
def revtoday():
    global todayData, runningAcc
    runningAcc = 'revtoday'
    data = request.form
    password = data['password']
    todayData = dbms.getTodayRevenue(password)
    return redirect(url_for('admin'))


@app.route('/admin/revenue/date', methods=['POST', 'GET'])
def revdate():
    global dateData, runningAcc
    runningAcc = 'revdate'
    data = request.form
    date = data['date']
    password = data['password']
    dateData = dbms.getDailyRevenue(password, date)
    return redirect(url_for('admin'))


@app.route('/admin/revenue/year', methods=['POST', 'GET'])
def revyear():
    global yearData, runningAcc
    runningAcc = 'revyear'
    data = request.form
    year = int(data['year'])
    password = data['password']
    yearData = dbms.getYearlyRevenue(password, year)
    return redirect(url_for('admin'))


@app.route('/admin/revenue/month', methods=['POST', 'GET'])
def revmonth():
    global monthData, runningAcc
    runningAcc = 'revmonth'
    data = request.form
    month = int(data['month'])
    year = int(data['year'])
    password = data['password']
    monthData = dbms.getMonthlyRevenue(password, year, month)
    return redirect(url_for('admin'))


@app.route('/admin/branch', methods=['POST', 'GET'])
def addbranch():
    global runningAcc
    runningAcc = 'addbranch'
    data = request.form
    shopName = data['shopname']
    shopAddress = data['shopaddress']
    dbms.setNewBranch((shopName, shopAddress))
    return redirect(url_for('admin'))


@app.route('/admin/employee', methods=['POST', 'GET'])
def addemployee():
    global runningAcc
    runningAcc = 'addemployee'
    data = request.form
    dbms.setNewEmployee((data['ename'], data['epassword'], str(data['phoneNumber']), data['edob'], data['eaddress']))
    return redirect(url_for('admin'))


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
