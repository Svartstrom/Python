


# index = login_required(index)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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


