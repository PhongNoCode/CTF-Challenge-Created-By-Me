import subprocess
import pymysql
from flask import Flask, render_template, request
import re
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/level_1', methods = ['POST', 'GET'])
def level1():
    result = ""
    if request.method == 'POST':
        try:
            userinput = request.form.get('command')
            pattern = r"[@'(),\\\t\n ]"
            if ('whoami' in userinput.lower()) or (len(re.findall(pattern, userinput.lower())) > 0):
                return render_template('index.html', Result = 'Quá gà')
            full_command = 'echo -e ' + userinput
            result = subprocess.getoutput(full_command)
        except Exception as e:
            return render_template('index.html', Result = e)
    return render_template('index.html', Result = result)






DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'ctf_db',
    'autocommit': True
}

def init():
    # Kết nối ban đầu để tạo database nếu chưa tồn tại
    con = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    with con.cursor() as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS ctf_db")
    con.close()

    con = pymysql.connect(**DB_CONFIG)
    with con.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(10),
                username VARCHAR(50),
                password VARCHAR(50)
            )
        """)
        cur.execute("DELETE FROM users")
        cur.execute("""
            INSERT INTO users VALUES
                ('1', 'admin', '7c6a180b36896a0a8c02787eeafb0e4c'),
                ('2', 'guest', 'fcea920f7412b5da7be0cf42b8c93759')
        """)
    con.close()

blacklist = [
    "or",
    "and",
    "union",
    "select",
    "like",
    "case",
    "when",
    "substr",
    "char",
    "instr",
    "cast",
    "sqlite_master"
]

@app.route('/level_2', methods=['POST', 'GET'])
def level2():
    username = ""
    password = ""
    result = ""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '')
            password = request.form.get('password', '')

            if re.search(r"[#,=|<>;\x00]", username):
                return render_template('index_2.html', Result='Quá gà')

            for word in blacklist:
                if word in username.lower() or word in password.lower():
                    return render_template('index_2.html', Result='Quá gà')

            res = hashlib.md5(password.encode())
            password_hex = res.hexdigest()

            full_command = f"SELECT * from users where username = '{username}' and password = '{password_hex}'"

            con = pymysql.connect(**DB_CONFIG)
            with con.cursor() as cur:
                cur.execute(full_command)
                
                result = cur.fetchall()
            con.close()

        except Exception as e:
            return render_template('index_2.html', Result=e)

    return render_template('index_2.html', Result=result)




if __name__ == '__main__':
    init()
    app.run()
