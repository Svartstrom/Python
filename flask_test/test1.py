from flask import Flask, render_template, g, request, redirect
import sqlite3 
from datetime import datetime

app = Flask(__name__)

DATABASE = 'test.db'
DATABASE_NAME = 'projects'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_database(name=None):
    if not name:
        name = DATABASE_NAME

    order = f'''CREATE TABLE IF NOT EXISTS {name} (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL,
                    date_created timestamp NOT NULL)'''
    cur = get_db().cursor()
    cur.execute(order)

@app.route('/delete/<int:id>')
def delete(id):
    cur = get_db().cursor()
    delete_order = f'''DELETE from {DATABASE_NAME} where id = {id}'''
    cur.execute(delete_order)
    get_db().commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    cur = get_db().cursor()
    if request.method == 'POST':
        task_content = request.form['content']
        update_order = f'''UPDATE {DATABASE_NAME} SET content = ? where id = {id}'''
        cur.execute(update_order, (task_content,))
        get_db().commit()
        return redirect('/')
    else:
        cur.execute(f'SELECT * FROM {DATABASE_NAME} WHERE id = {id}')
        row = cur.fetchall()
        return render_template('update.html', tasks=row)


def add_todo(content):
    cur = get_db().cursor()
    sql = f'''INSERT INTO {DATABASE_NAME}(content,date_created) VALUES(?,?) '''
    data = (content, datetime.utcnow().replace(microsecond=0))
    cur.execute(sql,data)
    get_db().commit()


@app.route("/", methods=['POST', 'GET'])
def hello_www():

    #cur = conn.cursor()
    create_database(DATABASE_NAME)

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = add_todo(content=task_content)
        return redirect('/')
    else:
        cur = get_db().cursor()
        cur.execute(f"SELECT * FROM {DATABASE_NAME}")
        #cur.commit()
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return render_template('main.html', tasks=rows)

@app.route('/about/')
def about():
    return render_template('about.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0')
