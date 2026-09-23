from flask import Flask, request, render_template
import subprocess
import re
app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to OS command injection"

@app.route('/level_1', methods=['POST', 'GET'])
def level_1():
    result = ""
    if request.method == "POST":
        try:
            userinput = request.form.get('command', "")
            full_command = 'ping -c 1 ' + userinput
            result = subprocess.check_output(full_command, shell=True)
        except:
            return render_template('index.html', command = 'Nhập theo mẫu: 127.0.0.1 hoặc google.com')
    return render_template('index.html', command = result)







@app.route('/level_2', methods=['POST', 'GET'])
def level_2():
    result = ""
    if request.method == "POST":
        try:
            userinput = request.form.get('command', "")
            pattern = r'[&|;]'
            if len(re.findall(pattern, userinput)) > 0:
                return render_template('index.html', command = 'Hành vi hack cực rõ :))')
            full_command = 'echo -e ' + userinput
            result = subprocess.check_output(full_command, shell=True)
        except:
            return render_template('index.html', command = 'Nhập theo mẫu: 127.0.0.1 hoặc google.com')
    return render_template('index.html', command = result)








@app.route('/level_3', methods=['POST', 'GET'])
def level_3():
    result = ""
    if request.method == "POST":
        try:
            userinput = request.form.get('command', "")
            pattern = r'[&|;` ]'
            if len(re.findall(pattern, userinput)) > 0:
                return render_template('index.html', command = 'Hành vi hack cực rõ :))')
            full_command = "echo -e " + userinput
            result = subprocess.check_output(full_command, shell=True)
        except:
            return render_template('index.html', command = 'Haizz, Hack chán thế')
    return render_template('index.html', command = result)







@app.route('/level_4', methods=['POST', 'GET'])
def level_4():
    result = ""
    if request.method == "POST":
        try:
            userinput = request.form.get('command', "")
            pattern = r'[&;\t() ]'
            if len(re.findall(pattern, userinput)) > 0 or 'whoami' in userinput.lower():
                return render_template('index.html', command = 'Hành vi hack cực rõ :))')
            full_command = "echo -e " + userinput
            result = subprocess.check_output(full_command, shell=True)
        except:
            return render_template('index.html', command = 'Haizz, Hack chán thế')
    return render_template('index.html', command = result)




if __name__ == '__main__':
    app.run()
