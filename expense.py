import sqlite3
import os
from flask import Flask,request,render_template,redirect
fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
conn=sqlite3.connect(fullpath)
curs=conn.cursor()

curs.execute(f"""
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    description TEXT,
    amttype TEXT)
    """)
conn.commit()
conn.close()

def addTransaction(amount,description,amttype):
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""
    INSERT INTO expenses(amount,description,amttype)
    VALUES(?,?,?)""",(amount,description,amttype))
    conn.commit()
    conn.close()
def viewTransactions():
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("SELECT * FROM expenses")
    data=curs.fetchall()
    conn.close()
    return data
def viewIncome():
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""SELECT * FROM expenses
                 WHERE amttype='income'""")
    data=curs.fetchall()
    conn.close()
    return data
def viewExpense():
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""SELECT * FROM expenses
                 WHERE amttype='expense'""")
    data=curs.fetchall()
    conn.close()
    return data  
def deleteTransaction(idn):
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""
                DELETE FROM expenses
                WHERE id=?""",(idn,))
    conn.commit()
    conn.close()
def totalExpenses():
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""SELECT amount FROM expenses
                 WHERE amttype='expense'""")
    data=curs.fetchall()
    num=0
    for row in data:
        num+=float(row[0])
    return num
def totalIncome():
    fullpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")
    conn=sqlite3.connect(fullpath)
    curs=conn.cursor()
    curs.execute("""SELECT amount FROM expenses
                 WHERE amttype='income'""")
    data=curs.fetchall()
    num=0
    for row in data:
        num+=float(row[0])
    return num
def checkLossProfit():
    income=totalIncome()
    expense=totalExpenses()
    if income>=expense:
        return "Profit"
    elif income<expense:
        return "Loss"

app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def home():
    check=checkLossProfit()
    checkvalue=0
    if check== "Profit":
        checkvalue=totalIncome()-totalExpenses()
    elif check== "Loss":
        checkvalue=totalExpenses()-totalIncome()
    if request.method=="POST":
        if "transactionpage" in request.form:
            return redirect("/transactions")
        elif "addpage" in request.form:
            return redirect("/add")
        elif "incomepage" in request.form:
            return redirect("/income")
        elif "expensepage" in request.form:
            return redirect("/expenses")
    return render_template("home.html",income=totalIncome(),expenses=totalExpenses(),check=check,checkvalue=checkvalue)
@app.route("/transactions",methods=["GET","POST"])
def transactions():
    if request.method=="POST":
        if "delete" in request.form:
            idn=request.form["delete"]
            deleteTransaction(idn)
        elif "home" in request.form:
            return redirect("/")
    alltran=viewTransactions()
    check=checkLossProfit()
    checkvalue=0
    if check== "Profit":
        checkvalue=totalIncome()-totalExpenses()
    elif check== "Loss":
        checkvalue=totalExpenses()-totalIncome()
    return render_template("transactions.html",income=totalIncome(),expenses=totalExpenses(),check=check,checkvalue=checkvalue,alltran=alltran)
@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        amount=request.form["amount"]
        description=request.form["description"]
        if "income" in request.form:
            addTransaction(amount,description,"income")
        elif "expense" in request.form:
            addTransaction(amount,description,"expense")
        elif "home" in request.form:
            return redirect("/")
    return render_template("add.html")
@app.route("/income",methods=["GET","POST"])
def income():
    if request.method=="POST":
        if "delete" in request.form:
            idn=request.form["delete"]
            deleteTransaction(idn)
        elif "home" in request.form:
            return redirect("/")
    allincome=viewIncome()
    return render_template("income.html",income=totalIncome(),allincome=allincome)
@app.route("/expenses",methods=["GET","POST"])
def expense():
    if request.method=="POST":
        if "delete" in request.form:
            idn=request.form["delete"]
            deleteTransaction(idn)
        elif "home" in request.form:
            return redirect("/")
    allexpense=viewExpense()
    return render_template("expenses.html",income=totalExpenses(),allexpense=allexpense)
app.run(debug=True)