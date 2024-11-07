from flask import Flask, render_template
from datetime import datetime
import locale

app = Flask(__name__)

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU')
except locale.Error:
    print("Ошибка")

@app.route('/')
def index():
    now = datetime.now()
    formatted_date = now.strftime("Сегодня %d %B %Y, сейчас %H:%M")
    return render_template('index.html', date_time=formatted_date)

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
