import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date

from helpers import apology, login_required, lookup, usd


def sumStocks(Uid):
    stocks = db.execute( "SELECT * FROM transactions WHERE Uid = :Uid", Uid  = session["user_id"] )
    master = {}
    for stock in stocks:
        if not stock['symbol'] in master:
            master[stock['symbol']] = {'price':0,'amount':0,'total':0}
        old_avg = master[stock['symbol']]['amount'] * master[stock['symbol']]['price']
        new_avg = stock['amount'] * stock['price']
        tot_amt = master[stock['symbol']]['amount'] + stock['amount']

        if tot_amt != 0:
            if new_avg > 0:
                master[stock['symbol']]['price'] = ( old_avg + new_avg ) / tot_amt
        else:
            master[stock['symbol']]['price'] = 0
        master[stock['symbol']]['amount'] += stock['amount']
        master[stock['symbol']]['total'] = master[stock['symbol']]['amount'] * master[stock['symbol']]['price']
    return master

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    DBcash = db.execute( "SELECT cash FROM users WHERE id = :Uid", Uid  = session["user_id"] )

    TOTAL_SUM = DBcash[0]['cash']
    DBcash[0]['cash'] = usd(DBcash[0]['cash'])
    M = sumStocks(session["user_id"])

    for stock in M:
        M[stock]['symbol'] = stock
        stock_info = lookup(M[stock]['symbol'])
        if not stock_info:
            apology("Database does not have contact with site for fetching prices")
        M[stock].update(stock_info)
        M[stock]['curr_total'] = M[stock]['price'] * M[stock]['amount']
        M[stock]['price'] = usd( M[stock]["price"] )
        TOTAL_SUM += M[stock]['total']
        M[stock]['curr_total'] = usd( M[stock]['curr_total'] )

    TOTAL_SUM = usd(TOTAL_SUM)
    N = {}
    for stock in M:
        if M[stock]['amount'] > 0:
            #print(f"M[stock]['symbol'] = {M[stock]['symbol']}")
            #print(f"M[stock] = {M[stock]}")

            N[M[stock]['symbol']] = M[stock]
    return render_template("index.html",DBcash=DBcash,DBstocks=N,TOTAL_SUM=TOTAL_SUM)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("No stock name submitted.",400)
        if not request.form.get("shares"):
            return apology("No stock amount submitted.",400)
        try:
            a = int(request.form.get("shares"))
        except:
            return apology("invalid amount of shares.",400)
        if (int(request.form.get("shares")) != int(request.form.get("shares"))//1) or int(request.form.get("shares")) < 0:
            return apology("invalid amount of shares.",400)
        stock_info = lookup(request.form.get("symbol"))

        if not stock_info:
            return apology("Could not find the stock",400)

        DBcash = db.execute( "SELECT cash FROM users WHERE id = :Uid", Uid  = session["user_id"] )
        tot_price = stock_info["price"] * int(request.form.get("shares"))

        if int(DBcash[0]['cash']) > tot_price:
            result = db.execute("INSERT INTO transactions (symbol,price,amount,date,Uid) VALUES(:symbol,:price,:amount, :date,:Uid)",
                            symbol=stock_info["symbol"], price=stock_info["price"], amount=request.form.get("shares"), date=datetime.now(), Uid=session["user_id"] )

            if not result:
                return apology("The transaction could not be completed.")
            else:
                db.execute("UPDATE users SET cash = cash - :tot_price where id = :Uid", tot_price = tot_price, Uid  = session["user_id"])
        else:
            return apology("Insufficient funds.")
        return redirect("/")
    else:
        return render_template("buy.html",symbol={"symbol":"Stock symbol"})

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute( "SELECT * FROM transactions WHERE Uid = :Uid", Uid  = session["user_id"] )

    for stock in stocks:
        stock_info = lookup(stock['symbol'])
        stock.update(stock_info)

    return render_template("history.html",DBstocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("No stock name submitted.",400)
        stock_info = lookup(request.form.get("symbol"))

        if not stock_info:
            return apology("Could not find the stock",400)
        stock_info["price"] = usd( stock_info["price"] )
        return render_template("showQuote.html",stock_info=stock_info)
    else:
        return render_template("quote.html")


@app.route("/showQuote", methods=["GET", "POST"])
@login_required
def showQuote():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("quote.html")#,stock_info=stock_info)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password twice!", 400)

        elif request.form.get("password") !=  request.form.get("confirmation"):
            return apology("Password and confirmation is not equal", 400)

        PWhash = generate_password_hash(request.form.get("password"))
        #PWhash = pwd_context.encrypt()
        result = db.execute( "INSERT INTO users (username,hash) VALUES(:username, :PWhash)",
                            username=request.form.get("username"),PWhash=PWhash )

        if not result:
            return apology("Username already excists",400)
        #return render_template("registerOK.html",username=request.form.get("Rusername"))
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


    #return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    DBcash = db.execute( "SELECT cash FROM users WHERE id = :Uid", Uid  = session["user_id"] )

    TOTAL_SUM = DBcash[0]['cash']
    DBcash[0]['cash'] = usd(DBcash[0]['cash'])
    M = sumStocks(session["user_id"])
    N = {}
    #print(M)
    for stock in M:
        if M[stock]['amount'] > 0:
            N[stock] = M[stock]
    #print(N)
    if request.method == "POST":
        #print("Sell Post")
        if not request.form.get("symbol"):
            return apology("No stock name submitted.",400)
        if not request.form.get("shares"):
            return apology("No stock amount submitted.",400)
        try:
            a = int(request.form.get("shares"))
        except:
            return apology("invalid amount of shares.",400)
        #if (int(request.form.get("shares")) != int(request.form.get("shares"))//1) or int(request.form.get("shares")) < 0:
        if  (int(request.form.get("shares")) != int(request.form.get("shares"))//1) or int(request.form.get("shares")) < 0:
            return apology("invalid amount of shares.",400)
        stock_info = lookup(request.form.get("symbol"))
        if not stock_info:
            return apology("Could not find the stock",400)
        if request.form.get("symbol") in M:
            if M[request.form.get("symbol")]['amount'] >= int(request.form.get("shares")):
                tot_price = stock_info["price"] * int(request.form.get("shares"))
                result = db.execute("INSERT INTO transactions (symbol,price,amount,date,Uid) VALUES(:symbol,:price,:amount, :date,:Uid)",
                            symbol=stock_info["symbol"], price=stock_info["price"], amount=-int(request.form.get("shares")), date=datetime.now(), Uid=session["user_id"] )
                if not result:
                    return apology("The transaction could not be completed.")
                else:
                    db.execute("UPDATE users SET cash = cash + :tot_price where id = :Uid", tot_price = tot_price, Uid  = session["user_id"])
            else:
                return apology("Not enuff shares to sell.",400)
            # TODO: write code...
        return redirect("/")
        #return render_template("sell.html",DBstocks=M)
    else:
        #print("Sell else")
        return render_template("sell.html",DBstocks=N)

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
