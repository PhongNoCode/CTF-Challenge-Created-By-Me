from flask import Flask, request, render_template
import sqlite3
import re

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my virtual lab"

def init():
    con = sqlite3.connect('sqli.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name varchar(30), password varchar(30))")
    cur.execute("""
    INSERT OR IGNORE INTO users VALUES
        (1, 'admin', 'adminpass'),
        (2, 'guest', 'guesspass')
""")
    con.commit()
    con.close()

@app.route('/level_1', methods = ['POST', 'GET'])
def login():
    userid = request.values.get('id', '')
    con = sqlite3.connect('sqli.db')
    cur = con.cursor()
    try:
        result = cur.execute(f"SELECT name FROM users WHERE id = '{userid}'").fetchall()
    except:
        return render_template("index_2.html", userid = f"Check carefully your query: SELECT name FROM users WHERE id = '{userid}'")
    finally:
        con.close()
    return render_template('index.html', userid=result)

@app.route('/level_2', methods = ['POST', 'GET'])
def login_safe():
    userid = request.values.get('id', '')
    pattern = r'[\x21-\x2f]'
    if len(re.findall(pattern, userid)) > 0:
        return render_template("index_2.html", userid = "Hack detected!!!")
    con = sqlite3.connect('sqli.db')
    cur = con.cursor()
    try:
        result = cur.execute(f"SELECT name FROM users WHERE id = {userid} order by id").fetchall()
    except:
        return render_template('index.html', userid = '')
    finally:
        con.close()
    return render_template('index.html', userid = result)
    
    
if __name__ == "__main__":
    init()
    app.run(debug=True)
