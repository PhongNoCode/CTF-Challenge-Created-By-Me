from flask import request, Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return 'Welcome to XSS challenge'


@app.route('/level_1', methods = ['POST', 'GET'])
def comment():
    if request.method == 'POST':
        comment = request.form['comment']
        
    return render_template('index.html')











BLACKLIST_LEVEL_2 = [
    '<script', '<body', '<img', '<svg', '<iframe', '<input', 
    '<audio', '<video', '<object', '<embed', '<a', '<details', 
    '<textarea', '<select', '<style', '<button', '<div', '<form', '<link', '<base'
]
@app.route('/level_2', methods = ['POST', 'GET'])
def comment_2():
    comment = ""

    for tag in BLACKLIST_LEVEL_2:
        if tag in request.values.get('comment', ''):
            return render_template('index_2.html', comment='Hack à bro ? Quay lại tìm cách khác đi nèo')

    if request.method == 'POST':
        
        comment = request.form['comment']
    
    return render_template('index_2.html', comment=comment)










BLACKLIST_LEVEL_3 = [
    '<script', '<body', '<img', '<svg', '<iframe', '<input', 
    '<audio', '<video', '<object', '<embed', '<a', '<details', 
    '<textarea', '<select', '<style', '<button', '<div', '<form', '<link', '<base', '<', '>', '"'
]
@app.route('/level_3', methods = ['POST', 'GET'])
def comment_3():
    link = ""
    for tag in BLACKLIST_LEVEL_3:
        if tag in request.values.get('link', '').lower():
            return render_template('index_3.html', link='kkk gà điên')
    if request.method == 'POST':
        link = request.form['link']
    return render_template('index_3.html', link=link)


if __name__ == '__main__':
    app.run()
