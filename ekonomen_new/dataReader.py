# coding=utf-8

from collections import deque
import glob
import sqlite3
import os
from openpyxl import load_workbook


def Table_exists(f):
        def wraper(*args, **kwargs):
                if "symbol" not in kwargs or "db" not in kwargs:
                        raise "CallingError"
                try:
                        db.execute("SELECT * from ? WHERE id=1;",kwargs["symbol"])
                except:
                        db.execute("CREATE TABLE ? ('date' DATE PRIMARY KEY UNIQUE, 
                        'list' TEXT, 'sector' TEXT, 'branch' TEXT, 'direktavkastning' INTEGER, 'pe' INTEGER, 'ps' INTEGER,'pb'INTEGER,
                        'openprice' INTEGER,'highprice'INTEGER,'lowprice'INTEGER, 'closeprice' INTEGER,'volume'INTEGER)",(kwargs["symbol"],))
                return f(*args, **kwargs)
        return wraper
                                   
@Table_exists
def insertBD(input_date, trade_list, sector, branch, dir_avk, pe,ps,pb,close_price,symbol,db):
        temp = db.execute("SELECT * FROM ? WHERE date=?;",(symbol,input_date))
        if temp:
                db.execute("UPDATE ? SET list=?, sector=?, branch=?, direktavkastning=?, pe=?, ps=?, pb=?,closeprice=? WHERE date=?",(symbol,trade_list,sector,branch,dir_avk,pe,ps,pb,close_price,input_date,))
        else:
                db.execute("INSERT INTO ? (datum, list,  sector, branch, direktavkastning, pe, ps, pb,closeprice) VALUES (?,?,?,?,?,?,?,?,?,?);",
                   (symbol, input_date, trade_list, sector, branch, dir_avk, pe, ps, pb, close_price))
@Table_exists
def insertTrades(input_date,open_price,high_price,low_price,close_price,volume,symbol,db):
        temp = db.execute("SELECT * FROM ? WHERE date=?;",(symbol,input_date))
        if temp:
                db.execute("UPDATE ? SET openprice=?, highprice=?,lowprice=?,closeprice=?,volume=? WHERE date=?;",(symbol,open_price,high_price,low_price,close_price,volume,input_date))
        else:
                db.execute("INSERT INTO ? (datum,openprice,highprice,lowprice,closeprice,volume) VALUES (?,?,?,?,?,?)",(symbol,input_date,open_price,high_price,low_price,close_price,volume))
                
# SELECT count(*) FROM sqlite_master WHERE type='table' AND name='table_name';
def createDatabase(DBname):
	db_ = sqlite3.connect(DBname)
	db  = db_.cursor()
	db.execute("""CREATE TABLE 'companies'('symbol' TEXT PRIMARY KEY UNIQUE, 
		      'datum' DATE, 'list' TEXT, 'sector' TEXT, 'branch' TEXT, 'direktavkastning' INTEGER, 'pe' INTEGER, 'ps' INTEGER, 'pb' INTEGER);""")
	db.execute("""CREATE TABLE 'transactions'(	'id' INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
                      'symbol' TEXT, 'datum' DATE, 'openprice' INTEGER,'highprice'INTEGER,'lowprice'INTEGER, 'closeprice' INTEGER,'volume'INTEGER );""")
	return db_

def readFromXLSX(db,ORGname,ij,max_ant):
	name = ORGname.split('/')[-1]
	name = name.replace("_","-")
	name = name.replace(".","-")
	name = name.split('-')

	wb = load_workbook(ORGname)
	ws = wb.active

	if name[0] == 'Borsdata':
                input_date = str(name[1])+"-"+str(name[2])+"-"+str(name[3])
                #Bolagsnamn	Info	Info	Info	Info	Info	Info		Info	Kursutveck.	Direktav.	P/E	P/S	P/B	Aktiekurs
		#		Land	Lista	Sektor	Bransch	Ticker	Instrument	Rapport	Utveck.  1 år	Senaste		Senaste	Senaste	Senaste	Senaste
                for row in ws.iter_rows(min_row = 3, min_col=1, max_row=ws.max_row, max_col=ws.max_col):
                        symbol = row[6].value
                        trade_list = row[3].value
		        sector  = row[4].value
		        branch  = row[5].value
		        dir_avk = row[10].value
		        pe = row[11].value
		        ps = row[12].value
		        pb = row[13].value
                        close_price = row[14].value
                        insertBD(input_date,trade_list,sector,branch,dir_avk,pe,ps,pb,close_price,symbol,db)
                # M-x comment-region
		# print("%s - %d out of of %d"%(name[0],ij,max_ant))
		# input_date = str(name[1])+"-"+str(name[2])+"-"+str(name[3])
                # #Bolagsnamn	Info	Info	Info	Info	Info	Info		Info	Kursutveck.	Direktav.	P/E	P/S	P/B	Aktiekurs
		# #		Land	Lista	Sektor	Bransch	Ticker	Instrument	Rapport	Utveck.  1 år	Senaste		Senaste	Senaste	Senaste	Senaste
		# for ii in range(3, ws.max_row):
		# 	name = [ws.cell(row = ii, column = 6).value]
		# 	temp = db.execute("SELECT * FROM companies WHERE symbol=? ",(name[0],))
		# 	tt = temp.fetchall()
		# 	#print(input_date)
		# 	lista   = ws.cell(row=ii, column = 3).value
		# 	sector  = ws.cell(row=ii, column = 4).value
		# 	branch  = ws.cell(row=ii, column = 5).value
		# 	dir_avk = ws.cell(row=ii, column = 10).value
		# 	pe = ws.cell(row=ii, column = 11).value
		# 	ps = ws.cell(row=ii, column = 12).value
		# 	pb = ws.cell(row=ii, column = 13).value
				
		# 	if len(tt) < 1:
		# 		resp = db.execute("""INSERT INTO companies (symbol,  datum, list,  sector, branch, direktavkastning, pe, ps, pb) VALUES (?,?,?,?,?,?,?,?,?);""",
                #                                   (name[0], input_date, lista, sector, branch, dir_avk, pe, ps, pb))

		# 	else:
		# 		resp = db.execute("""UPDATE companies SET datum = ?, list = ?,  sector = ?, branch = ?, direktavkastning = ?, pe = ?, ps = ?, pb = ? WHERE symbol = ? ;""",
                #                                   (input_date, lista, sector, branch, dir_avk, pe, ps, pb, name[0]))
		# 		#print("Borsdata To late.")
		# 	temp = db.execute("SELECT * FROM transactions WHERE symbol=? AND datum=?",(name[0],input_date))
		# 	tt= temp.fetchall()
		# 	if len(tt) < 1:
		# 		close_price = ws.cell(row=ii, column = 14).value
		# 		resp = db.execute("""INSERT INTO transactions (symbol, datum, closeprice) VALUES (?,?,?);""",
                #                                   (name[0], input_date, close_price) )
	else:
                for row in ws.iter_rows(min_row = 2, min_col=1, max_row=ws.max_row, max_col=ws.max_col):
                        input_date  = row[1].value.date()
                        open_price  = row[2].value
                        high_price  = row[3].value
                        low_price   = row[4].value
                        close_price = row[5].value
                        volume = row[6].value
                        symbol = name[0]
                        insertTrades(input_date,open_price,high_price,low_price,close_price,volume,symbol,db)
		# resp = db.execute("SELECT symbol from companies WHERE symbol=?",(name[0],))
		# #if len(resp) < 1:
		# print("%s - %d out of of %d"%(name[0],ij,max_ant))
		# for ii in range(2,ws.max_row):
		# 	try:
		# 		input_date  = ws.cell(row=ii, column = 1).value.date()
		# 	except:
		# 		print(ws.cell(row=ii, column = 1).value)
		# 		continue
		# 	# check that the transaction is not already in DB
		# 	temp = db.execute("SELECT * FROM transactions WHERE symbol=? AND datum=?",(name[0],input_date))
		# 	tt= temp.fetchall()
		# 	if len(tt) < 1:
		# 		# Date	Openprice	Highprice	Lowprice	Closeprice	Volume	| MA15	MA50	MA200	DMA15	DMA50	DMA200
				
		# 		open_price  = ws.cell(row=ii, column = 2).value
		# 		high_price  = ws.cell(row=ii, column = 3).value
		# 		low_price   = ws.cell(row=ii, column = 4).value
		# 		close_price = ws.cell(row=ii, column = 5).value
		# 		volume      = ws.cell(row=ii, column = 6).value
		# 		resp = db.execute("""INSERT INTO transactions ( symbol,  datum,      openprice,  highprice,  lowprice,  closeprice,  volume) 
		# 							VALUES (?,?,?,?,?,?,?);""",(name[0], input_date, open_price, high_price, low_price, close_price, volume))
		# 	else:
		# 		pass#print(tt)
		# 		#print("To late.")

def testeerr(db):
	os.system("rm -f ekonomen_test.db")
	db_ = createDatabase("ekonomen_test.db")
	#db = SQL("sqlite:///ekonomen_test.db")
	ij = 1

	temp = db.execute("select * from transactions;")
	#print(temp.fetchall())
	for ii in range(400):
		resp = db.execute("SELECT id FROM transactions WHERE id=?;",(ii,))
		for d in resp.fetchall():
			#if len(d) > 0:
			pass#print("id is %d"%d[0])#['rowid'])
			#DBcash = db.execute( '''SELECT 1 FROM main WHERE  name=:table_name''', {'table_name' : name} )
			#cursor.execute('''INSERT INTO users(name, phone, email, password)
		#  VALUES(?,?,?,?)''', (name1,phone1, email1, password1))
			#DBcash = db.execute('''create table if not exists :name''',{name=name})#TableName (col1 typ1, ..., colN typN)
			#try:
		#resp = db.execute("INSERT INTO main (symbol,longname) VALUES (?,'aaaaaaa');",(name,))
			#DBcash = db.execute( 'SELECT 1 FROM  main WHERE  table_name=?', name )
				#DBcash = db.execute( 'SELECT 1 FROM  information_schema.tables WHERE  table_name=:table_name', {'table_name' : name} )
			#	print(DBcash)
			#except sqlite3.OperationalError:
			#print("Fail")
			#DBcash = db.execute( "SELECT cash FROM users WHERE id = :Uid", Uid  = session["user_id"] )
			
			#2
			#cursor.execute('''INSERT INTO users(name, phone, email, password)
		#VALUES(:name,:phone, :email, :password)''',
		#  {'name':name1, 'phone':phone1, 'email':email1, 'password':password1})

def main():
	#os.system("rm -f ekonomen.db")
	resp = glob.glob("ekonomen.db")
	if len(resp) < 1:
		db_ = createDatabase("ekonomen.db")
	else:
		db_ = sqlite3.connect("ekonomen.db")
	db = db_.cursor()
	db_.commit()
	db_.close()
	ij = 1

	full_list = glob.glob("Data_full/G*.xlsx")
	for ORGname in full_list:
		db_ = sqlite3.connect("ekonomen.db")
		db = db_.cursor()
		#db_.commit()
		#db_.close()
		readFromXLSX(db,ORGname,ij,len(full_list))
		ij+=1
		#tester(db)
		os.system("rm -f " + ORGname)
		db_.commit()
		db_.close()

if __name__ == "__main__":
	main()
