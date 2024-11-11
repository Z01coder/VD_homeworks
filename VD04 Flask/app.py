from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import locale

app = Flask(__name__)

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU')
except locale.Error:
    print("Ошибка")

# Хранилище анкет
user_data = []


@app.route('/')
def index():
    now = datetime.now()
    formatted_date = now.strftime("Сегодня %d %B %Y, сейчас %H:%M")
    return render_template('index.html', date_time=formatted_date)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    global user_data
    if request.method == 'POST':
        # Достаем данные из формы
        name = request.form.get('name')
        city = request.form.get('city')
        hobby = request.form.get('hobby')
        age = request.form.get('age')

        # Пополняем хранилище анкет
        user_data.append({
            'name': name,
            'city': city,
            'hobby': hobby,
            'age': age
        })

        # Редирект
        return redirect(url_for('blog'))

    return render_template('blog.html', user_data=user_data)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
